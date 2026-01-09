from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth import get_user_model


# Регистрация кастомной модели пользователя в админке
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    '''
    - Кастомная админка под модель без username.
    - Перенастраиваем поля и формы, чтобы работало создание/редактирование.
    '''
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    # Форма, так как username удалён, собираем набор полей вручную
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'middle_name')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'middle_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


User = get_user_model() # Возвращает актуальный класс пользователя, указанный в AUTH_USER_MODEL, именно account.CustomUser


class UserInfoAdminMixin:
    '''
    Общие методы для отображения связанных данных пользователя:
    - Email
    - Имя
    - Фамилия
    '''

    # Декоратор: отображает email связанного пользователя в списке профилей учеников
    @admin.display(description='Email', ordering='user__email')
    def user_email(self, obj):
        return obj.user.email

    # Декоратор: отображает имя связанного пользователя в списке профилей учеников
    @admin.display(description='Имя', ordering='user__first_name')
    def user_first_name(self, obj):
        return obj.user.first_name

    # Декоратор: отображает фамилию связанного пользователя в списке профилей учеников
    @admin.display(description='Фамилия', ordering='user__last_name')
    def user_last_name(self, obj):
        return obj.user.last_name
