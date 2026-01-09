from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    # Вход
    path('login/', views.user_login, name='login'), # Доступен всем
    
    # Выход
    path('logout/', views.user_logout, name='logout'), # Доступен всем
    
    # Регистрация
    path('registry/', views.registry, name='registry'), # Доступен всем
    # Активация
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # Уведомление об отправке письма с активацией
    path('activation-sent/', views.activation_sent, name='activation_sent'), # Доступен всем
    # Успешная активация
    path('activation-end/', views.activation_end, name='activation_end'), # Доступен всем
    # Невалидная/просроченная активация
    path('activation-invalid/', views.activation_invalid, name='activation_invalid'), # Доступен всем
    
    # Изменение пароля
    path('password-change/', views.password_change, name='password_change'), # Доступен только авторизованным, неавторизованных перенаправляет на страницу входа
    # Успешное изменение пароля
    path('password-change/done/', views.password_change_done, name='password_change_done'), # Доступен только авторизованным, неавторизованных перенаправляет на страницу входа
    
    # Сброс пароля
    path('password-reset/', views.password_reset, name='password_reset'), # Доступен всем, сделан редирект для авторизованных
    # Успешный сброс пароля
    path('password-reset/done/', views.password_reset_end, name='password_reset_end'), # Доступен всем
    # Подтверждение сброса пароля
    path('password-reset/<slug:uidb64>/<slug:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # Завершение сброса пароля
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'), # Доступен всем

    # VK OAuth
    path('oauth/vk/start/', views.oauth_vk_start, name='oauth_vk_start'),
    path('oauth/vk/reg/', views.oauth_vk_reg, name='oauth_vk_reg'),
    path('oauth/vk/callback/', views.oauth_vk_callback, name='oauth_vk_callback'),
    path('oauth/confirm-link/', views.oauth_vk_confirm_link, name='oauth_vk_confirm_link'),

    # Yandex OAuth
    path('oauth/yandex/start/', views.oauth_yandex_start, name='oauth_yandex_start'),
    path('oauth/yandex/reg/', views.oauth_yandex_reg, name='oauth_yandex_reg'),
    path('oauth/yandex/callback/', views.oauth_yandex_callback, name='oauth_yandex_callback'),
    path('oauth/yandex/confirm-link/', views.oauth_yandex_confirm_link, name='oauth_yandex_confirm_link'),
]