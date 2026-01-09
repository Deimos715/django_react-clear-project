from django.contrib.auth import authenticate
from rest_framework import serializers


'''
Логин по email/паролю.

    - Принимаем email + password.
    - Проверяем пользователя через authenticate().
    - Возвращаем user (в validated_data), если всё ок.
'''
