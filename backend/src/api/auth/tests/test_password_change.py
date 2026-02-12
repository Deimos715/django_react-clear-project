from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class PasswordChangeAPITestCase(APITestCase):
    '''
    Тесты API смены пароля пользователя.

    Проверяем поведение POST /api/auth/password-change/.

    Сценарии:

    1. Успешная смена пароля:
       - HTTP 200 OK.
       - Пароль пользователя изменяется в базе данных.
       - Старый пароль становится недействительным.
       - Новый пароль корректно проходит validate_password.

    2. Неверный старый пароль:
       - HTTP 400 Bad Request.
       - Ошибка приходит в поле "old_password".

    3. Несовпадающие новые пароли:
       - HTTP 400 Bad Request.
       - Ошибка приходит в поле "new_password2".

    4. Новый пароль не проходит validate_password
       (например, слишком короткий):
       - HTTP 400 Bad Request.
       - Ошибка приходит в поле "new_password1".
       - Сообщение ошибки соответствует контракту сериализатора.

    5. Неавторизованный пользователь:
       - HTTP 401 Unauthorized.
       - Запрос блокируется на уровне permission до сериализатора.

    Цель тестов:
    - Зафиксировать контракт API смены пароля.
    - Защитить поведение при рефакторинге сериализатора или view.
    - Гарантировать корректную работу validate_password.
    '''
    def setUp(self):
        self.password = 'StrongPass123!@#'
        self.user = User.objects.create_user(
            email = 'test@example.com',
            password=self.password,
            first_name='Test_first_name',
            last_name='Test_last_name',
            middle_name = 'Test_middle_name',
        )

        self.url = reverse('api:auth:password-change')
        self.client.force_authenticate(user=self.user)

    def test_password_change_success_returns_200(self):
        response = self.client.post(
            self.url,
            {'old_password': self.password,
            'new_password1': 'NewStrongPass123!@#',
            'new_password2': 'NewStrongPass123!@#',
            },
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Обновление объекта пользователя из БД
        self.user.refresh_from_db()
        # Проверка, что новый пароль действительно установлен
        self.assertTrue(self.user.check_password('NewStrongPass123!@#'))
        # Проверка, что старый пароль больше не работает
        self.assertFalse(self.user.check_password(self.password))

    def test_password_change_wrong_old_password_returns_400(self):
        response = self.client.post(
            self.url,
            {'old_password': 'wrong-old_password',
            'new_password1': 'NewStrongPass123!@#',
            'new_password2': 'NewStrongPass123!@#',
            },
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка, что ошибка пришла в поле old_password
        self.assertIn('old_password', response.data)
        # Проверка текста ошибки
        self.assertIn('Старый пароль неверный.', response.data['old_password'])

    def test_password_change_password_mismatch_returns_400(self):
        response = self.client.post(
            self.url,
            {'old_password': self.password,
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

    def test_password_change_short_new_password_returns_400(self):
        response = self.client.post(
            self.url,
            {'old_password': self.password,
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

    def test_password_change_unauthorized_returns_401(self):
        self.client.force_authenticate(user = None)
        response = self.client.post(
            self.url,
            {'old_password': self.password,
             'new_password1': 'NewStrongPass123!@#',
             'new_password2': 'NewStrongPass123!@#',
            },
            format='json',
        )

        # Проверка статуса
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

