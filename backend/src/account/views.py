from django.conf import settings
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from .tokens import account_activation_token


# Константы и choices
User = get_user_model()


class ActivateAccountView(View):
    '''
    Активация учётной записи по ссылке из email.

    Поведение:
    - активируем пользователя
    - ставим refresh cookie
    - редиректим на React-страницы результата
    '''

    def get(self, request, uidb64, token):
        frontend_url = settings.FRONTEND_URL.rstrip('/')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return redirect(frontend_url + '/activation/invalid/')

        if not account_activation_token.check_token(user, token):
            return redirect(frontend_url + '/activation/invalid/')

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])

        refresh = RefreshToken.for_user(user)

        response = redirect(frontend_url + '/activation/success/')

        response.set_cookie(
            key=settings.JWT_REFRESH_COOKIE_NAME,
            value=str(refresh),
            httponly=settings.JWT_REFRESH_COOKIE_HTTPONLY,
            secure=getattr(settings, 'JWT_REFRESH_COOKIE_SECURE', True),
            samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
            path=settings.JWT_REFRESH_COOKIE_PATH,
        )
        return response
