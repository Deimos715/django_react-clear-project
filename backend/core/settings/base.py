import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Секретный ключ
SECRET_KEY = os.getenv('SECRET_KEY')


# Sita id
SITE_ID = 1


# Своя модель пользователя
AUTH_USER_MODEL = 'account.CustomUser'


# CORS
CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = True


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # user apps
    'src.account.apps.AccountConfig',

    # REST
    'rest_framework',
    'rest_framework_simplejwt',

    # CORS
    'corsheaders',

    # api
    'src.api.apps.ApiConfig',

    # Other apps

    # sitemaps
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # robots
    'robots',
]


# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}


# JWT настройки
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'LEEWAY': 30,
}


# Cookies
JWT_REFRESH_COOKIE_NAME = 'refresh_token'
JWT_REFRESH_COOKIE_HTTPONLY = True
JWT_REFRESH_COOKIE_SAMESITE = 'Lax'
JWT_REFRESH_COOKIE_PATH = '/api/auth/'


# AUTHENTICATION_BACKENDS определяет список бэкендов аутентификации, которые Django будет использовать
# 'django.contrib.auth.backends.ModelBackend' — стандартный бэкенд Django,
# который проверяет учетные данные (email/username + пароль) через модель пользователя,
# а также обрабатывает права доступа (is_active, is_staff, is_superuser, группы, разрешения).
# Если в списке оставить только этот бэкенд, вход возможен только через пользователей,
# хранящихся в базе Django, без сторонних систем авторизации.
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']


MIDDLEWARE = [
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'


# Database SQLite, для режима development (расскоментировать при зобычном запуске с SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# PostgreSQL, для режима development/production (расскоментировать при запуске через Docker
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT'),
#     }
# }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    # Стандартные валидаторы паролей Django отключены, так как используются кастомные валидаторы
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # Отключен, так как используется кастомный валидатор
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

    # Кастомные валидаторы паролей
    {
        'NAME': 'src.account.validators.CustomMinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
]


# Internationalization
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'


# Directory definition for static
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Defining the base directory for collecting staticfiles
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# URL-имя (name из urls.py), на который Django будет перенаправлять
# незалогиненного пользователя при попытке доступа к @login_required вьюхе.
# Django автоматически добавит параметр ?next=... для возврата после входа.
# LOGIN_URL = '#' # используется только для session-based auth (не используется)


# URL-имя, куда Django отправит пользователя после успешного входа,
# если в запросе не был передан параметр next.
# Используется, например, во встроенном LoginView или при ручном redirect().
# Пока на main:index
# LOGIN_REDIRECT_URL = '#' # используется только для session-based auth (не используется)


# Настройки для отправки почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mail.ru')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465))
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'True') == 'True'
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_TIMEOUT = 20
