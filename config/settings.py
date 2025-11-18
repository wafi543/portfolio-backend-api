import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta
import dj_database_url
from corsheaders.defaults import default_headers, default_methods

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, 'environments', '.env'))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', os.getenv('DJANGO_SECRET_KEY', ''))  # Replace with your actual variable name

DEBUG = os.environ.get('DJANGO_DEBUG', os.getenv('DJANGO_DEBUG', 'True')) == 'True'

CURRENT_ENV = 'local' # local - test - prod

ALLOWED_HOSTS: list = [
    'localhost',
    '127.0.0.1',
    'https://pixel-portfolios.vercel.app'
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    "https://pixel-portfolios.vercel.app"
]
CORS_PREFLIGHT_MAX_AGE = 0
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = default_headers + (
    "custom-headers",
)
CORS_ALLOWED_METHODS = default_methods
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://pixel-portfolios.vercel.app"
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework',
    'corsheaders',
    'posts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
if CURRENT_ENV == 'prod':
    LOCAL_SETUP_DATABASE = os.getenv('PROD_DATABASE_URL')
elif CURRENT_ENV == 'test':
    LOCAL_SETUP_DATABASE = os.getenv('TEST_DATABASE_URL')
else:
    LOCAL_SETUP_DATABASE = os.getenv('LOCAL_DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL', LOCAL_SETUP_DATABASE))
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')