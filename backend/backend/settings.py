"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5ku3tfr%jfod2m-06u^q6^63(v4&2=mg4lle!n(k@)vkb$d$tz'

TOKEN_EXPIRATION_TIME = 36000

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = [
	'corsheaders',
	'daphne',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'api',
	'frontend',
	'channels',
	'rest_framework',
	'rest_framework_simplejwt',
	'django_otp',
	'django_otp.plugins.otp_totp',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
	'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

ASGI_APPLICATION = 'backend.asgi.application'

CHANNEL_LAYERS = { 
	"default": {
		"BACKEND": "channels.layers.InMemoryChannelLayer"
	}   
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.getenv('POSTGRES_DB'),
		'USER': os.getenv('POSTGRES_USER'),
		'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
		'HOST': os.getenv('DB_HOST'),
		'PORT': os.getenv('DB_PORT'),
	}
}

AUTH_USER_MODEL = 'api.User'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Password hashing
# https://docs.djangoproject.com/en/5.0/topics/auth/passwords/

PASSWORD_HASHERS = [
	"django.contrib.auth.hashers.PBKDF2PasswordHasher",
	"django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
	"django.contrib.auth.hashers.Argon2PasswordHasher",
	"django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
	"django.contrib.auth.hashers.ScryptPasswordHasher",
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

APPEND_SLASH=False

CSRF_COOKIE_HTTPONLY = False

CORS_ALLOW_HEADERS = [
	'X-CSRFToken', 
	'content-type',
	'Authorization'
]

CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_SECURE = True

ip_value = os.getenv('IP')
CSRF_TRUSTED_ORIGINS = [
  f'https://{ip_value}:8000',
  'https://10.12.4.8:8000'
]

CORS_TRUSTED_ORIGINS = [
	f'https://{ip_value}:8000',
	'https://10.12.4.8:8000'
]

CORS_ALLOWED_ORIGINS = [
	f'https://{ip_value}:8000',
	'https://10.12.4.8:8000',
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# JWT Token

REST_FRAMEWORK = {
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	),
}

SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
	'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
	'SLIDING_TOKEN_LIFETIME': timedelta(days=2),
	'ROTATE_REFRESH_TOKENS': False,
	'ALGORITHM': 'HS256',
	'SIGNING_KEY': SECRET_KEY,
}