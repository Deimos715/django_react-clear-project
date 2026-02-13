from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class PasswordResetStartAPITestCase(APITestCase):
	'''
    Тесты API запроса восстановления пароля.

    Проверяем поведение POST /api/auth/password-reset/.

    Сценарии:

    1. Существующий email:
       - HTTP 200 OK.
       - Ответ не раскрывает существование пользователя.
       - Письмо отправляется.

    2. Несуществующий email:
       - HTTP 200 OK.
       - Ответ идентичен случаю существующего email.
       - Письмо не отправляется.

    Цель тестов:
    - Зафиксировать контракт API.
    - Исключить user enumeration.
    '''
	def setUp(self):
		self.password = 'StrongPass123!@#'
		self.user = User.objects.create_user(
			email = 'test@example.com',
			password = self.password,
			first_name='Test_first_name',
            last_name='Test_last_name',
            middle_name = 'Test_middle_name',
		)

		self.url = reverse('api:auth:password-reset-start')

	# Проверка существующего email
	def test_password_reset_start_existing_email_returns_200(self):
		response = self.client.post(
			self.url,
			{
				'email': self.user.email,
			},
			format='json',
		)