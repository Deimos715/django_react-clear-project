from django.urls import path, include
from .views import (
    ActivateAccountView,
)

app_name = 'account'

urlpatterns = [
    # Активация
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
]