from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
# INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
# MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
]

# Cookies
JWT_REFRESH_COOKIE_SECURE = False
