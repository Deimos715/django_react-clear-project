from django.urls import path

from .views import LoginAPIView, RefreshAPIView, LogoutAPIView, RegisterAPIView

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
]