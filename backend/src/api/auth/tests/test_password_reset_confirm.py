from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()

class PasswordResetConfirmAPITestCase(APITestCase):
    '''
    Тесты API подтверждения восстановления пароля.

    Проверяем поведение POST /api/auth/password-reset/confirm/.

    Сценарии:

    1. Успешное подтверждение:
       - HTTP 200 OK.
       - Пароль пользователя изменяется.

    2. Несовпадающие пароли:
       - HTTP 400 Bad Request.
       - Ошибка приходит в поле "new_password2".

    3. Невалидный token или uidb64:
       - HTTP 400 Bad Request.
       - Ошибка приходит в поле "token".

    4. Новый пароль не проходит validate_password:
       - HTTP 400 Bad Request.
       - Ошибка приходит в поле "new_password1".
    '''
    def setUp(self):
        # Тестовый пользователь (должен быть активным, иначе serializer не найдёт его)
        self.password = 'StrongPass123!@#'
        self.user = User.objects.create_user(
            email='test@example.com',
            password=self.password,
            first_name='Test_first_name',
            last_name='Test_last_name',
            middle_name='Test_middle_name',
        )
        self.user.is_active = True
        self.user.save(update_fields=['is_active'])
        self.url = reverse('api:auth:password-reset-confirm')

        # Валидные uidb64/token для успешного сценария
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)

    # Успешное подтверждение
    def test_password_reset_confirm_success_returns_200_and_changes_password(self):
        new_password = 'NewStrongPass123!@#'

        response = self.client.post(
            self.url,
            {
                'uidb64': self.uidb64,
                'token': self.token,
                'new_password1': new_password,
                'new_password2': new_password,
            },
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка текста ответа
        self.assertEqual(response.data['detail'], 'Пароль успешно изменён.')
        # Обновление пользователя из БД
        self.user.refresh_from_db()
        # Проверка, что новый пароль установлен
        self.assertTrue(self.user.check_password(new_password))
        # Проверка, что старый пароль больше не работает
        self.assertFalse(self.user.check_password(self.password))

    # Несовпадающие пароли
    def test_password_reset_confirm_password_mismatch_returns_400(self):
        response = self.client.post(
            self.url,
            {
                'uidb64': self.uidb64,
                'token': self.token,
                'new_password1': 'NewStrongPass123!@#',
                'new_password2': 'DifferentStrongPass123!@#',
            },
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле new_password2
        self.assertIn('new_password2', response.data)
        # Проверка текста ошибки
        self.assertIn('Пароли не совпадают.', response.data['new_password2'])

    # Невалидный token
    def test_password_reset_confirm_invalid_token_returns_400(self):
        response = self.client.post(
            self.url,
            {
                'uidb64': self.uidb64,
                'token': 'invalid-token',
                'new_password1': 'NewStrongPass123!@#',
                'new_password2': 'NewStrongPass123!@#',
            },
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле token
        self.assertIn('token', response.data)
        # Проверка текста ошибки
        self.assertIn('Ссылка недействительна или устарела.', response.data['token'])

    # Невалидный uidb64
    def test_password_reset_confirm_invalid_uidb64_returns_400(self):
        response = self.client.post(
            self.url,
            {
                'uidb64': 'invalid-uidb64',
                'token': self.token,
                'new_password1': 'NewStrongPass123!@#',
                'new_password2': 'NewStrongPass123!@#',
            },
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле token
        self.assertIn('token', response.data)
        # Проверка текста ошибки
        self.assertIn('Ссылка недействительна или устарела.', response.data['token'])

    # Новый пароль не проходит validate_password
    def test_password_reset_confirm_short_password_returns_400(self):
        response = self.client.post(
            self.url,
            {
                'uidb64': self.uidb64,
                'token': self.token,
                'new_password1': 'Pass!@#',
                'new_password2': 'Pass!@#',
            },
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле new_password1
        self.assertIn('new_password1', response.data)
        # Проверка текста ошибки
        self.assertIn('Пароль слишком короткий', response.data['new_password1'][0])