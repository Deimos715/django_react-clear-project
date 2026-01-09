from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LoginSerializer


class LoginAPIView(APIView):
    '''
    POST /api/auth/login/

    Описание:
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

    Описание:
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

            resp.set_cookie(
                key=cookie_name,
                value=str(refresh),
                httponly=settings.JWT_REFRESH_COOKIE_HTTPONLY,
                secure=getattr(settings, "JWT_REFRESH_COOKIE_SECURE", False),
                samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
                path=settings.JWT_REFRESH_COOKIE_PATH,
            )

        return resp


class LogoutAPIView(APIView):
    '''
    POST /api/auth/logout/

    Описание:
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