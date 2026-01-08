from django.urls import path, include
from .views import HomeAPIView

app_name = 'api'

urlpatterns = [
    path('home/', HomeAPIView.as_view(), name='home'),
]