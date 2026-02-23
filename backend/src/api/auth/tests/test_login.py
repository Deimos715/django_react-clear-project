from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class LoginAPITestCase(APITestCase):
    '''
    Тесты API логина пользователя.

    Проверяем поведение POST /api/auth/login/:

    Сценарии:
    1. Успешный вход:
    - Возвращается HTTP 200.
    - В JSON присутствует access-токен.
    - В cookie устанавливается refresh-токен
    с корректными флагами из settings.

    2. Неверный пароль:
    - Возвращается HTTP 400.
    - Ошибка приходит в non_field_errors.

    3. Неактивный пользователь:
    - Возвращается HTTP 400.
    - Ошибка приходит в non_field_errors.

    Цель тестов:
    - Зафиксировать контракт API логина.
    - Защитить поведение при рефакторинге сериализатора или view.
    '''
    def setUp(self):
        self.password = 'StrongPass123!@#'
        self.user = User.objects.create_user(
            email = 'test@example.com',
            password = self.password,
            first_name = 'Test_first_name',
            last_name = 'Test_last_name',
            middle_name = 'Test_middle_name',
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])

        self.url = reverse('api:auth:login')
    
    # Успешный вход
    def test_login_success_returns_access_and_sets_refresh_cookie(self):
        response = self.client.post(
            self.url,
            {'email': 'test@example.com', 'password': self.password},
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка, что в ответе присутствует access-токен
        self.assertIn('access', response.data)
        # Проверка, что access-токен не пустой
        self.assertTrue(response.data['access'])

        # Получаем имя refresh-cookie из настроек
        cookie_name = settings.JWT_REFRESH_COOKIE_NAME
        # Проверка, что refresh-cookie установлена
        self.assertIn(cookie_name, response.cookies)
        # Достаём саму cookie
        cookie = response.cookies[cookie_name]
        
        # Проверка флаг HttpOnly (безопасность: недоступна из JS)
        self.assertEqual(bool(cookie["httponly"]), bool(settings.JWT_REFRESH_COOKIE_HTTPONLY))
        # Проверка атрибута SameSite
        self.assertEqual(cookie["samesite"], settings.JWT_REFRESH_COOKIE_SAMESITE)
        # Проверка пути cookie
        self.assertEqual(cookie["path"], settings.JWT_REFRESH_COOKIE_PATH)
        # Проверка флага Secure (зависит от dev/prod настроек)
        self.assertEqual(bool(cookie["secure"]), bool(settings.JWT_REFRESH_COOKIE_SECURE))

    # Неверный пароль
    def test_login_wrong_password_returns_400(self):
        response = self.client.post(
            self.url,
            {'email': 'test@example.com', 'password': 'wrong-password'},
            format='json',
        )
        
        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в общем поле non_field_errors
        self.assertIn("non_field_errors", response.data)
        # Проверка, что текст ошибки соответствует контракту API
        self.assertIn("Неверный логин или пароль.", response.data["non_field_errors"])

    # Неактивный пользователь
    def test_login_inactive_user_returns_400(self):
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])

        response = self.client.post(
            self.url,
            {'email': 'test@example.com', 'password': self.password},
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в общем поле non_field_errors
        self.assertIn("non_field_errors", response.data)
        # Проверка, что текст ошибки соответствует контракту API
        self.assertIn("Неверный логин или пароль.", response.data["non_field_errors"])