from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework import serializers

# Модель пользователя
User = get_user_model() # Возвращает актуальный класс пользователя, указанный в AUTH_USER_MODEL, именно account.CustomUser


class LoginSerializer(serializers.Serializer):
    '''
    Логин по email/паролю.

    Поведение:
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



class RegisterSerializer(serializers.ModelSerializer):
    '''
    Регистрация пользователя.

    Поведение:
    - создаём пользователя через User.objects.create_user(...)
    - is_active будет False по умолчанию (см. модель пользователя)
    - пароль валидируем через AUTH_PASSWORD_VALIDATORS
    (включая кастомный CustomMinimumLengthValidator из src.account.validators)
    - после регистрации JWT не выдаём (это будет в views)
    '''
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password2 = serializers.CharField(write_only=True, trim_whitespace=False)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'middle_name'
        )

    def validate_email(self, value):
        email = (value or '').strip().lower()
        if not email:
            raise serializers.ValidationError('Введите email.')
        
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует.')
        
        return email

    def validate_first_name(self, value):
        first_name = (value or '').strip()
        if not first_name:
            raise serializers.ValidationError('Введите имя.')
        return first_name

    def validate_last_name(self, value):
        last_name = (value or '').strip()
        if not last_name:
            raise serializers.ValidationError('Введите фамилию.')
        return last_name

    def validate_middle_name(self, value):
        middle_name = (value or '').strip()
        if not middle_name:
            raise serializers.ValidationError('Введите отчество.')
        return middle_name
    
    def validate(self, attrs):
        password = attrs.get('password') or ''
        password2 = attrs.get('password2') or ''

        if password != password2:
            raise serializers.ValidationError({'password2': 'Пароли не совпадают.'})

        # Валидируем пароль через AUTH_PASSWORD_VALIDATORS
        # (включая кастомный валидатор длины из settings.py) :contentReference[oaicite:1]{index=1}
        user = User(
            email=(attrs.get('email') or '').strip().lower(),
            first_name=(attrs.get('first_name') or '').strip(),
            last_name=(attrs.get('last_name') or '').strip(),
            middle_name=(attrs.get('middle_name') or '').strip(),
        )

        try:
            validate_password(password=password, user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')

        email = (validated_data.pop('email') or '').strip().lower()

        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                **validated_data,
            )
        except IntegrityError:
            # Другой запрос успел создать пользователя с этим email
            raise serializers.ValidationError(
                {"email": "Пользователь с таким email уже существует."}
            )

        return user

