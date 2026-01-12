import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LoginSerializer, RegisterSerializer, PasswordChangeSerializer, PasswordResetConfirmSerializer
from rest_framework.permissions import IsAuthenticated

from .serializers import PasswordResetStartSerializer

from src.account.tokens import account_activation_token

logger = logging.getLogger(__name__)

# Модель пользователя
User = get_user_model() # Возвращает актуальный класс пользователя, указанный в AUTH_USER_MODEL, именно account.CustomUser


class ActivationEmailError(Exception):
    pass


class LoginAPIView(APIView):
    '''
    POST /api/auth/login/

    Поведение:
    - refresh кладём в HttpOnly cookie
    - access возвращаем в JSON
    '''
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        resp = Response(
            data={
                'access': access_token,
            },
            status=status.HTTP_200_OK,
        )

        # refresh cookie
        resp.set_cookie(
            key=settings.JWT_REFRESH_COOKIE_NAME,
            value=str(refresh),
            httponly=settings.JWT_REFRESH_COOKIE_HTTPONLY,
            secure=getattr(settings, 'JWT_REFRESH_COOKIE_SECURE', True),
            samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
            path=settings.JWT_REFRESH_COOKIE_PATH,
        )
        return resp


class RefreshAPIView(APIView):
    '''
    POST /api/auth/refresh/

    Поведение:
    - refresh берём из HttpOnly cookie
    - выдаём новый access в JSON
    - при ROTATE_REFRESH_TOKENS=True: выдаём новый refresh и обновляем cookie
    '''
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        cookie_name = settings.JWT_REFRESH_COOKIE_NAME
        refresh_str = request.COOKIES.get(cookie_name)

        if not refresh_str:
            return Response(
                {"detail": "Refresh cookie not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_str)
        except TokenError:
            # refresh битый/протух — удаляем cookie, чтобы клиент не зацикливался
            resp = Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            resp.delete_cookie(
                key=cookie_name,
                path=settings.JWT_REFRESH_COOKIE_PATH,
            )
            return resp

        # Новый access
        access_token = str(refresh.access_token)

        resp = Response(
            {"access": access_token},
            status=status.HTTP_200_OK,
        )

        # Ротация refresh (по твоему SIMPLE_JWT: ROTATE_REFRESH_TOKENS=True)
        if getattr(settings, "SIMPLE_JWT", {}).get("ROTATE_REFRESH_TOKENS", False):
            # refresh после rotate меняется (объект обновится)
            refresh.set_jti()
            refresh.set_exp()
            
            # refresh cookie
            resp.set_cookie(
                key=cookie_name,
                value=str(refresh),
                httponly=settings.JWT_REFRESH_COOKIE_HTTPONLY,
                secure=getattr(settings, "JWT_REFRESH_COOKIE_SECURE", True),
                samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
                path=settings.JWT_REFRESH_COOKIE_PATH,
            )

        return resp


class LogoutAPIView(APIView):
    '''
    POST /api/auth/logout/

    Поведение:
    - удаляем refresh cookie (HttpOnly)
    '''
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        cookie_name = settings.JWT_REFRESH_COOKIE_NAME

        resp = Response(status=status.HTTP_204_NO_CONTENT)
        resp.delete_cookie(
            key=cookie_name,
            path=settings.JWT_REFRESH_COOKIE_PATH,
        )
        return resp


class RegisterAPIView(APIView):
    '''
    POST /api/auth/register/

    Поведение:
    - создаём пользователя (is_active=False по CustomUserManager)
    - отправляем письмо с активацией
    - JWT НЕ выдаём (пользователь ещё не активирован)
    - Если письмо подтверждения не отправилось — откатываем транзакцию,
    пользователь не остаётся "висеть" в БД, и возвращаем 503.
    '''
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                # 1) Создаём пользователя (менеджер ставит is_active=False)
                user = serializer.save()

                # 2) Генерируем ссылку активации
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)

                activation_url = request.build_absolute_uri(
                    reverse("account:activate", kwargs={"uidb64": uid, "token": token})
                )

                # 3) Рендерим HTML письма
                subject = "Активация личного кабинета на сайте"
                html = render_to_string(
                    "account/activation_email.html",
                    {
                        "user": user,
                        "activation_url": activation_url,
                        "uid": uid,
                        "token": token,
                    },
                )

                # 4) Отправляем письмо
                email = EmailMessage(subject, html, to=[user.email])
                email.content_subtype = "html"
                try:
                    email.send(fail_silently=False)
                except Exception as exc:
                    logger.exception("Failed to send activation email")
                    raise ActivationEmailError() from exc

        except ActivationEmailError:
            return Response(
                {
                    "detail": "Не удалось отправить письмо подтверждения. Попробуйте позже.",
                    "code": "activation_email_not_sent",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {"detail": "Регистрация успешна. Проверьте почту и подтвердите аккаунт."},
            status=status.HTTP_201_CREATED,
        )


class PasswordChangeAPIView(APIView):
    '''
    POST /api/auth/password-change/

    Поведение:
    - требуем access (Bearer) => IsAuthenticated
    - меняем пароль (проверяя old_password)
    - выдаём новый refresh в HttpOnly cookie
    - возвращаем новый access в JSON
    - опционально: пытаемся заблэклистить старый refresh (если включён blacklist)
    '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        new_password = serializer.validated_data['new_password1']

        # Опционально: blacklist старого refresh из cookie (если есть и если включён token_blacklist)
        cookie_name = settings.JWT_REFRESH_COOKIE_NAME
        old_refresh_str = request.COOKIES.get(cookie_name)
        if old_refresh_str:
            try:
                old_refresh = RefreshToken(old_refresh_str)
                if hasattr(old_refresh, "blacklist"):
                    old_refresh.blacklist()
            except TokenError:
                # старый refresh уже мог быть битый/протухший — просто игнорируем
                pass

        # Меняем пароль
        user.set_password(new_password)
        user.save(update_fields=['password'])

        # Выдаём новую пару токенов
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        resp = Response({"access": access_token}, status=status.HTTP_200_OK)

        resp.set_cookie(
            key=settings.JWT_REFRESH_COOKIE_NAME,
            value=str(refresh),
            httponly=settings.JWT_REFRESH_COOKIE_HTTPONLY,
            secure=getattr(settings, "JWT_REFRESH_COOKIE_SECURE", True),
            samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
            path=settings.JWT_REFRESH_COOKIE_PATH,
        )
        return resp


class PasswordResetStartAPIView(APIView):
    '''
    Запрос письма для восстановления пароля.

    POST /api/auth/password-reset/

    Поведение:
    - принимаем email
    - если пользователь найден — шлём письмо со ссылкой на backend redirect-view
    - всегда отвечаем 200 (не раскрываем существование email)
    '''
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_str = serializer.validated_data['email']

        user = User.objects.filter(email__iexact=email_str, is_active=True).first()

        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                reverse(
                    'account:password-reset-redirect',
                    kwargs={'uidb64': uidb64, 'token': token},
                )
            )

            subject = 'Восстановление пароля'
            html = render_to_string(
                "account/password_reset_email.html",
                {
                    'user': user,
                    'reset_link': reset_link,
                    'uidb64': uidb64,
                    'token': token,
                }
            )

            msg = EmailMessage(subject, html, to=[user.email])
            msg.content_subtype = "html"

            try:
                msg.send(fail_silently=False)
            except Exception:
                logger.exception("Failed to send password reset email")

        return Response(
            {'detail': 'Если такой email существует, мы отправили письмо для восстановления.'},
            status=status.HTTP_200_OK,
        )
    

class PasswordResetConfirmAPIView(APIView):
    '''
    Подтверждение восстановления пароля.

    POST /api/auth/password-reset/confirm/

    Поведение:
    - принимаем uidb64/token и новый пароль
    - проверяем токен
    - ставим новый пароль
    - JWT НЕ выдаём (после reset обычно просим войти заново)
    '''
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {"detail": "Пароль успешно изменён."},
            status=status.HTTP_200_OK,
        )