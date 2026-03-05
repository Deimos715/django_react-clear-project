import os
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import FileExtensionValidator
from .validators import phone_regex, validate_not_future
from django.db import transaction




class CustomUserManager(BaseUserManager):
    '''
    - Менеджер для модели пользователя.
    - Знает, как создавать обычных пользователей и суперпользователей,
    когда логинимся по email (а не по username).
    '''
    # Позволяет использовать этот менеджер в миграциях
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # Внутренний метод для создания пользователя (общая логика)
        if not email:
            raise ValueError('Требуется email')
        email = self.normalize_email(email)  # Приводим email к нормализованному виду
        user = self.model(email=email, **extra_fields)  # Создаём экземпляр пользователя
        user.set_password(password)  # Хэшируем пароль
        user.save(using=self._db)  # Сохраняем в БД
        return user

    def create_user(self, email, password=None, **extra_fields):
        # Создание обычного пользователя, неактивный по умолчанию (ученик)
        extra_fields.setdefault('is_staff', False)  # Не админ
        extra_fields.setdefault('is_superuser', False)  # Не суперпользователь
        extra_fields.setdefault('is_active', False)  # Неактивный, для подтверждения через почту
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        # Создание суперпользователя, активный
        extra_fields.setdefault('is_staff', True)  # Доступ в админку
        extra_fields.setdefault('is_superuser', True)  # Полные права
        extra_fields.setdefault('is_active', True)  # Активный

        # Проверка, чтобы суперпользователь обязательно был staff и superuser
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser должен иметь is_superuser=True')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    '''
    Основная модель пользователя:
    - убираем username: по ТЗ он не нужен для логина
    - делаем email уникальным и используем его как USERNAME_FIELD
    - оставляем first_name/last_name из AbstractUser
    - добавляем middle_name, и флаг ученика по ТЗ
    '''
    username = None # полностью отключаем username
    email = models.EmailField(unique=True, verbose_name='Email') # Логинимся по email, username отключаем
    first_name = models.CharField(max_length=150, blank=False, verbose_name='Имя') # По ТЗ поле обязательное, переопределяем AbstractUser
    last_name = models.CharField(max_length=150, blank=False, verbose_name='Фамилия') # По ТЗ поле обязательное, переопределяем AbstractUser
    middle_name = models.CharField(max_length=150, verbose_name='Отчество') # ФИО: first_name/last_name уже есть в AbstractUser, добавляем только отчество 

    USERNAME_FIELD = 'email' # Логинимся по email
    REQUIRED_FIELDS = [] # В createsuperuser запросит только email и пароль

    objects = CustomUserManager()

    # Метод для получения полного имени пользователя
    def get_full_name(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(p for p in parts if p).strip()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


def _soft_strip(val: str) -> str:
    '''
    - Мягкая нормализация строк: NBSP -> пробел и обрезка по краям.
    '''
    if not isinstance(val, str):
        return val
    return val.replace('\u00A0', ' ').strip()