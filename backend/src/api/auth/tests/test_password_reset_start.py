from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core import mail

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

		self.user.is_active = True
		self.user.save(update_fields=['is_active'])
		self.url = reverse('api:auth:password-reset-start')

	# Существующий email
	def test_password_reset_start_existing_email_returns_200(self):
		response = self.client.post(
			self.url,
			{
				'email': self.user.email,
			},
			format='json',
		)

		# Проверка статуса
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# Проверка, что ответ не раскрывает существование пользователя
		self.assertEqual(response.data['detail'], 'Если такой email существует, мы отправили письмо для восстановления.')
		# Проверка, что письмо отправляется
		self.assertEqual(len(mail.outbox), 1)
		# Проверка, что письмо отправлено на email пользователя
		self.assertEqual(mail.outbox[0].to, [self.user.email])

	# Несуществующий email
	def test_password_reset_start_non_existing_email_returns_200(self):
		response = self.client.post(
			self.url,
			{
				'email': 'nonexistent@example.com'
			},
			format='json',
		)