import os
from datetime import timedelta
from pathlib import Path

import environ
from django.core.exceptions import ImproperlyConfigured


DJANGO_TEST = os.environ.get('DJANGO_TEST', False)
root = environ.Path(__file__) - 1
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
if not DJANGO_TEST:
  environ.Env.read_env(os.path.join(BASE_DIR, f'.env'))

APP_NAME = env.str('APP_NAME')
APP_DOMAIN = env.str('APP_DOMAIN')
SECRET_KEY = env.str('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env.tuple('ALLOWED_HOSTS', default=['localhost', '0.0.0.0'])
CORS_ORIGIN_ALLOW_ALL = env.bool('CORS_ORIGIN_ALLOW_ALL', default=False)
CORS_ORIGIN_WHITELIST = env.tuple(
  'CORS_ORIGIN_WHITELIST',
  default=('https://localhost:8000', 'https://0.0.0.0:8000',))

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django_extensions',
  'corsheaders',
  'rest_framework',
  'rest_framework_simplejwt.token_blacklist',
  'core.apps.CoreConfig',
  'api.apps.ApiConfig',
  'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
  'whitenoise.middleware.WhiteNoiseMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATE_DIR = BASE_DIR.parent / env.str('DJANGO_TEMPLATE_DIR')
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [TEMPLATE_DIR],
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [
  BASE_DIR.parent / env.str('DJANGO_STATIC_DIR')
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

"""
Cookie HttpOnly
"""
LANGUAGE_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

"""
Reference
=========
https://github.com/jacobian/dj-database-url
"""
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': env.str('POSTGRES_DB'),
    'USER': env.str('POSTGRES_USER'),
    'PASSWORD': env.str('POSTGRES_PASSWORD'),
    'HOST': env.str('POSTGRES_HOST'),
    'PORT': env.str('POSTGRES_PORT'),
    'TEST': {
      'NAME': 'postgres_test',
      'MIRROR': 'default',
    },
  },
}

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'default': {
      'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    },
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'level': 'INFO',
      'formatter': 'default',
      'stream': 'ext://sys.stdout',
    },
    'file': {
      'class': 'logging.FileHandler',
      'level': 'INFO',
      'formatter': 'default',
      'filename': env.str('LOGGER_FILE_PATH', default='/var/log/application.log'),
    },
  },
  'loggers': {
    '': {
      'handlers': env.list('LOGGER_HANDLERS', default=['file']),
      'level': env.str('LOGGER_LEVEL', default='INFO'),
      'propagate': False,
    },
    'django': {
      'handlers': env.list('LOGGER_HANDLERS', default=['file']),
      'level': env.str('LOGGER_LEVEL', default='INFO'),
      'propagate': False,
    },
  },
}

""" Settings for rest_framework """
REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
  ],
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ],
  'DEFAULT_THROTTLE_CLASSES': [
    'rest_framework.throttling.AnonRateThrottle',
    'rest_framework.throttling.UserRateThrottle',
  ],
  'DEFAULT_THROTTLE_RATES': {
    'anon': env.str('DRF_THROTTLE_RATES_ANONYMOUS'),
    'user': env.str('DRF_THROTTLE_RATES_USER'),
  },
  'EXCEPTION_HANDLER': 'api.resources.exception_handler.custom_exception_handler',
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE': 10,
}

""" Settings for Auth (django.contrib.auth) """
AUTH_USER_MODEL = 'core.User'
AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

""" Settings for rest_framework_simplejwt """
SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(
      minutes=env.int('ACCESS_TOKEN_LIFETIME_MINS')),
  'REFRESH_TOKEN_LIFETIME': timedelta(
      days=env.int('REFRESH_TOKEN_LIFETIME_DAYS')),
  'ALGORITHM': 'HS256',
  'AUTH_HEADER_TYPES': ('Bearer',),
  'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION', # Will accept 'Authorization'
  'USER_ID_FIELD': 'id',
  'UPDATE_LAST_LOGIN': env.bool('UPDATE_LAST_LOGIN'),
}

""" Settings for email """
EMAIL_VERIFICATION_CODE_LENGTH = env.int('EMAIL_VERIFICATION_CODE_LENGTH')
EMAIL_VERIFICATION_CODE_LIFETIME_MINS = env.int('EMAIL_VERIFICATION_CODE_LIFETIME_MINS')

EMAIL_BACKEND = env.str('EMAIL_BACKEND')
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env.str('EMAIL_PORT')
EMAIL_USE_TLS = env.str('EMAIL_USE_TLS')

""" Settings for media. """
MEDIA_ROOT = os.path.join(BASE_DIR, env.str('MEDIA_ROOT'))
MEDIA_URL = env.str('MEDIA_URL')

""" Setings for APIs. """
TENANT_DOMAIN_LENGTH = env.int('TENANT_DOMAIN_LENGTH')
TENANT_INVITATION_CODE_LENGTH = env.int('TENANT_INVITATION_CODE_LENGTH')
TENANT_INVITATION_CODE_LIFETIME_MINS = (
    env.int('TENANT_INVITATION_CODE_LIFETIME_MINS'))
TENANT_INVITATION_CODE_REQUEST_MAX_SIZE = (
    env.int('TENANT_INVITATION_CODE_REQUEST_MAX_SIZE'))

FAILED_LOGIN_ATTEMPT_MAX_COUNT = env.int('FAILED_LOGIN_ATTEMPT_MAX_COUNT')
LOGIN_LOCK_PERIOD_MINS = env.int('LOGIN_LOCK_PERIOD_MINS')
PASSWORD_RESET_CODE_LENGTH = env.int('PASSWORD_RESET_CODE_LENGTH')
PASSWORD_RESET_CODE_LIFETIME_MINS = env.int('PASSWORD_RESET_CODE_LIFETIME_MINS')
