from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework import serializers

User = get_user_model()

class RegisterAPITestCase(APITestCase):
    '''
 Тесты API регистрации пользователя.

    Проверяем поведение POST /api/auth/register/.

    Сценарии:

    1. Успешная регистрация:
       - HTTP 201 Created.
       - Пользователь создаётся в базе.
       - По умолчанию пользователь создаётся с is_active=False
         (активация выполняется отдельно).

    2. Регистрация с уже существующим email:
       - HTTP 400 Bad Request.
       - Ошибка приходит в поле "email".

    3. Регистрация с несовпадающими паролями (password != password2):
       - HTTP 400 Bad Request.
       - Ошибка приходит в поле "password2".

    4. Регистрация с паролем, не проходящим validate_password (например, слишком короткий):
       - HTTP 400 Bad Request.
       - Ошибка приходит в поле "password".

    5. Регистрация с пустыми обязательными полями (first_name/last_name/middle_name):
       - HTTP 400 Bad Request.
       - Ошибка приходит в соответствующее поле.
       - Текст ошибки — стандартная валидация DRF для blank-значений.

    Цель тестов:
    - Зафиксировать контракт API регистрации (статусы и структура ошибок).
    - Защитить поведение при рефакторинге сериализатора и/или view.
    '''
    def setUp(self):
        self.password = 'StrongPass123!@#'

        self.valid_payload = {
            'email': 'test@example.com',
            'password': self.password,
            'password2': self.password,
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name',
            'middle_name': 'Test_middle_name',
        }

        self.url = reverse('api:auth:register')

    def test_register_success_creates_user(self):
        response = self.client.post(
            self.url,
            {'email': 'test@example.com',
             'password': self.password,
             'password2': self.password, 
             'first_name': 'Test_first_name',
             'last_name': 'Test_last_name',
             'middle_name': 'Test_middle_name',
            },
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверка, что пользователь создан
        self.assertTrue(User.objects.filter(email="test@example.com").exists())
        # Проверка is_active
        user = User.objects.get(email="test@example.com")
        self.assertFalse(user.is_active)

    def test_register_existing_email_returns_400(self):
        User.objects.create_user(
            email = self.valid_payload['email'],
            password='StrongPass123!@#'
        )

        response = self.client.post(
            self.url,
            self.valid_payload,
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле email
        self.assertIn('email', response.data)
        # Проверка текста ошибки для уже существующего email
        self.assertIn('Пользователь с таким email уже существует.', response.data['email'])

    def test_register_password_mismatch_returns_400(self):
        data = self.valid_payload.copy()
        data['password2'] = 'DifferentStrongPass123!@#'

        response = self.client.post(
            self.url,
            data,
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле password2
        self.assertIn('password2', response.data)
        # Проверка текста ошибки
        self.assertIn('Пароли не совпадают.', response.data['password2'])

    def test_register_short_password_returns_400(self):
        data = self.valid_payload.copy()
        data['password'] = 'Pass!@#'
        data['password2'] = 'Pass!@#'

        response = self.client.post(
            self.url,
            data,
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле password
        self.assertIn('password', response.data)
        # Проверка текста ошибки
        self.assertIn('Пароль слишком короткий', response.data['password'][0])

    def test_register_empty_first_name_returns_400(self):
        data = self.valid_payload.copy()
        data['first_name'] = ''

        response = self.client.post(
            self.url,
            data,
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле first_name
        self.assertIn('first_name', response.data)
        # Проверка текста ошибки
        self.assertIn('Это поле не может быть пустым.', response.data['first_name'])

    def test_register_empty_last_name_returns_400(self):
        data = self.valid_payload.copy()
        data['last_name'] = ''

        response = self.client.post(
            self.url,
            data,
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле last_name
        self.assertIn('last_name', response.data)
        # Проверка текста ошибки
        self.assertIn('Это поле не может быть пустым.', response.data['last_name'])

    def test_register_empty_middle_name_returns_400(self):
        data = self.valid_payload.copy()
        data['middle_name'] = ''

        response = self.client.post(
            self.url,
            data,
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле middle_name
        self.assertIn('middle_name', response.data)
        # Проверка текста ошибки
        self.assertIn('Это поле не может быть пустым.', response.data['middle_name'])