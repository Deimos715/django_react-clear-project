from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RefreshAPITestCase(APITestCase):
    '''
    Тесты API обновления access токена.

    Проверяем поведение POST /api/auth/refresh/.

    Поведение:
    - refresh берём из HttpOnly cookie
    - выдаём новый access в JSON
    - при ROTATE_REFRESH_TOKENS=True: выдаём новый refresh и обновляем cookie

    Сценарии:

    1. Нет refresh cookie:
       - HTTP 401 Unauthorized.
       - detail = "Refresh cookie not found."

    2. Невалидный refresh token:
       - HTTP 401 Unauthorized.
       - detail = "Invalid refresh token."
       - refresh cookie удаляется (delete_cookie).

    3. Валидный refresh token:
       - HTTP 200 OK.
       - access присутствует в ответе.

    4. ROTATE_REFRESH_TOKENS=True:
       - refresh cookie обновляется (значение меняется).

    5. ROTATE_REFRESH_TOKENS=False:
       - refresh cookie не устанавливается заново (нет Set-Cookie в ответе).
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

        self.url = reverse('api:auth:refresh')
        self.cookie_name = settings.JWT_REFRESH_COOKIE_NAME

    # Нет refresh cookie
    def test_refresh_without_cookie_returns_401(self):
        response = self.client.post(self.url, {}, format='json')

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Проверка текста ошибки
        self.assertEqual(response.data['detail'], 'Refresh cookie not found.')

    # Невалидный refresh token
    def test_refresh_with_invalid_token_returns_401_and_deletes_cookie(self):
        self.client.cookies[self.cookie_name] = 'invalid-refresh-token'

        response = self.client.post(self.url, {}, format='json')

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Проверка текста ошибки
        self.assertEqual(response.data['detail'], 'Invalid refresh token.')
        # Проверка, что cookie удаляется
        self.assertIn(self.cookie_name, response.cookies)
        self.assertEqual(response.cookies[self.cookie_name].value, '')

    # Валидный refresh token
    def test_refresh_with_valid_token_returns_200_and_access(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies[self.cookie_name] = str(refresh)

        response = self.client.post(self.url, {}, format='json')

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка, что access выдан
        self.assertIn('access', response.data)
        self.assertTrue(bool(response.data['access']))

    # ROTATE_REFRESH_TOKENS=True
    def test_refresh_rotate_refresh_tokens_true_updates_cookie(self):
        rotate = getattr(settings, "SIMPLE_JWT", {}).get("ROTATE_REFRESH_TOKENS", False)
        if not rotate:
            self.skipTest('ROTATE_REFRESH_TOKENS=False')

        refresh = RefreshToken.for_user(self.user)
        old_refresh_str = str(refresh)
        self.client.cookies[self.cookie_name] = old_refresh_str

        response = self.client.post(self.url, {}, format='json')

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка, что refresh cookie обновлён
        self.assertIn(self.cookie_name, response.cookies)
        new_refresh_str = response.cookies[self.cookie_name].value
        self.assertTrue(bool(new_refresh_str))
        self.assertNotEqual(new_refresh_str, old_refresh_str)

    # ROTATE_REFRESH_TOKENS=False
    def test_refresh_rotate_refresh_tokens_false_does_not_set_cookie(self):
        rotate = getattr(settings, "SIMPLE_JWT", {}).get("ROTATE_REFRESH_TOKENS", False)
        if rotate:
            self.skipTest('ROTATE_REFRESH_TOKENS=True')

        refresh = RefreshToken.for_user(self.user)
        self.client.cookies[self.cookie_name] = str(refresh)

        response = self.client.post(self.url, {}, format='json')

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка, что cookie не переустанавливается в ответе
        self.assertNotIn(self.cookie_name, response.cookies)