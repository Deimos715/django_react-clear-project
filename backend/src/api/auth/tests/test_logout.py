from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class LogoutAPITestCase(APITestCase):
    '''
    Тесты API выхода (logout).

    Проверяем поведение POST /api/auth/logout/.

    Поведение:
    - удаляем refresh cookie (HttpOnly)
    - возвращаем 204 No Content
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
        self.url = reverse('api:auth:auth-logout')
        self.cookie_name = settings.JWT_REFRESH_COOKIE_NAME

    # Нет refresh cookie
    def test_logout_without_cookie_returns_204_and_deletes_cookie(self):
        response = self.client.post(self.url, {}, format='json')

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверка, что cookie удаляется
        self.assertIn(self.cookie_name, response.cookies)
        self.assertEqual(response.cookies[self.cookie_name].value, '')

    # Есть refresh cookie
    def test_logout_with_cookie_returns_204_and_deletes_cookie(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies[self.cookie_name] = str(refresh)

        response = self.client.post(self.url, {}, format='json')

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверка, что cookie удаляется
        self.assertIn(self.cookie_name, response.cookies)
        self.assertEqual(response.cookies[self.cookie_name].value, '')