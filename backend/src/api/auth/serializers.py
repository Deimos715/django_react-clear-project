from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    '''
    Логин по email/паролю.
    - Принимаем email + password.
    - Проверяем пользователя через authenticate().
    - Возвращаем user (в validated_data), если всё ок.
    '''
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = (attrs.get('email') or '').strip().lower()
        password = attrs.get('password') or ''

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Неверный логин или пароль.')

        if not getattr(user, 'is_active', False):
            raise serializers.ValidationError('Аккаунт не активирован.')

        attrs['user'] = user
        return attrs
