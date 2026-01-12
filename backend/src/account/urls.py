from django.urls import path, include
from .views import (
    ActivateAccountView,
    PasswordResetRedirectView
)

app_name = 'account'

urlpatterns = [
    # Активация
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

    # Восстановление пароля
    path('password-reset/redirect/<uidb64>/<token>/', PasswordResetRedirectView.as_view(), name='password-reset-redirect'),
]