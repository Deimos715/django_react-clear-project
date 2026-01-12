from django.urls import path

from .views import LoginAPIView, RefreshAPIView, LogoutAPIView, RegisterAPIView, PasswordChangeAPIView, PasswordResetStartAPIView, PasswordResetConfirmAPIView

app_name = 'auth'

urlpatterns = [
    # POST /api/auth/login/
    path('login/', LoginAPIView.as_view(), name='login'),

    # POST /api/auth/refresh/
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),

    # POST /api/auth/logout/
    path('logout/', LogoutAPIView.as_view(), name='auth-logout'),

    # POST /api/auth/register/
    path('register/', RegisterAPIView.as_view(), name='register'),

    # POST /api/auth/password-change/
    path('password-change/', PasswordChangeAPIView.as_view(), name='password-change'),

    # POST /api/auth/password-reset/
    path('password-reset/', PasswordResetStartAPIView.as_view(), name='password-reset-start'),

    # POST /api/auth/password-reset/confirm/
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
]