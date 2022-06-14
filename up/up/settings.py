"""
Django settings for up project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import logging
import os
import sys
from pathlib import Path

import dj_database_url
import environ
from django.core.management.utils import get_random_secret_key


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# ROOT_DIR = Path(__file__).resolve().parent.parent.parent
from upapp.utils.logger import setLogger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', cast=bool, default=False)
IS_DOCKER = env('IS_DOCKER', cast=bool, default=False)
IS_DEV = env('IS_DEV', cast=bool, default=True)

LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logger = setLogger(LOG_LEVEL)

PREPEND_WWW = False  # not DEBUG
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost,0.0.0.0').split(',')
if LEVER_LOCAL_URL_OVERRIDE := env('LEVER_LOCAL_URL_OVERRIDE', default=None):
    ALLOWED_HOSTS.append(LEVER_LOCAL_URL_OVERRIDE)

CSRF_USE_SESSIONS = True

logger.info(f'Base directory is: {BASE_DIR}')

# Application definition

INSTALLED_APPS = [
    'upapp.apps.UpAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.sites',
    'django.contrib.sitemaps',
    'manifest_loader',
    'storages',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'upapp.middleware.UserMiddleware',
]

ROOT_URLCONF = 'up.urls'
# SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'up/../upapp/templates')],
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

WSGI_APPLICATION = 'up.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if DEBUG is True:
    logger.info('CURRENTLY IN DEBUG MODE')
    if env('DB') == 'local':
        logger.info('Using local')
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': env('LOCAL_DB_NAME'),
                'USER': env('DB_USER'),
                'PASSWORD': env('DB_PASSWORD'),
                'HOST': 'db' if IS_DOCKER else 'localhost',
                'PORT': 5432
            }
        }
    elif env('DB') == 'dev':
        logger.info('Using dev db')
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'defaultdb',
                'USER': env('DB_DEV_USER'),
                'PASSWORD': env('DB_DEV_PASSWORD'),
                'HOST': 'db-postgresql-nyc3-30775-do-user-9892554-0.b.db.ondigitalocean.com',
                'PORT': 25060
            }
        }
    elif env('DB') == 'prod':
        logger.info('Using prod db')
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'db',
                'USER': env('DB_PROD_USER'),
                'PASSWORD': env('DB_PROD_PASSWORD'),
                'HOST': 'app-28bfbbdf-5450-4caa-8d8a-72df00331a57-do-user-9892554-0.b.db.ondigitalocean.com',
                'PORT': 25060
            }
        }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    logger.info('CURRENTLY IN PRODUCTION MODE')
    logger.info('System arguments:')
    for arg in sys.argv:
        logger.info(arg)
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }


LEVER_SCOPE = ' '.join([
    'archive_reasons:read:admin',
    'contact:read:admin',
    'notes:write:admin',
    'opportunities:write:admin',
    'postings:read:admin',
    'stages:read:admin',
    'tags:read:admin',
    'users:read:admin',
    'webhooks:write:admin',
    'offline_access'
])
LEVER_CALLBACK_URL = '/integrate'
LEVER_CLIENT_ID = env('LEVER_CLIENT_ID')
LEVER_CLIENT_SECRET = env('LEVER_CLIENT_SECRET')
LEVER_STATE = env('LEVER_STATE')

if LEVER_DEBUG := env('LEVER_DEBUG', cast=bool, default=True):
    LEVER_BASE_URL = 'https://api.sandbox.lever.co/v1/'
    LEVER_REDIRECT_BASE = 'https://sandbox-lever.auth0.com/authorize'
    LEVER_AUTH_TOKEN_URL = 'https://sandbox-lever.auth0.com/oauth/token'
else:
    LEVER_BASE_URL = 'https://api.lever.co/v1/'
    LEVER_REDIRECT_BASE = 'https://auth.lever.co/authorize'
    LEVER_AUTH_TOKEN_URL = 'https://auth.lever.co/oauth/token'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'up.multiPartJsonParser.MultiPartJsonParser',
    ]
}


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'up/frontend/dist'),
    os.path.join(BASE_DIR, 'up/static'),
]

logger.info(f'STATIC DIRS: {STATICFILES_DIRS}')

MANIFEST_LOADER = {
    'output_dir': None,  # where webpack outputs to, if not set, will search in STATICFILES_DIRS for the manifest.
    'manifest_file': 'manifest.json',  # name of your manifest file
    'cache': not DEBUG,  # recommended True for production, requires a server restart to pick up new values from the manifest.
}


def logListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    # Iterate over all the entries
    for entry in os.listdir(dirName):
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            logger.info(fullPath)

logger.info('File paths from up')
logListOfFiles(os.path.join(BASE_DIR, 'up'))

logger.info('File paths from frontend')
logListOfFiles(os.path.join(BASE_DIR, 'up/frontend'))

AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_ACCESS_KEY_ID_READ_ONLY = os.getenv('AWS_ACCESS_KEY_ID_READ_ONLY')
AWS_SECRET_ACCESS_KEY_READ_ONLY = os.getenv('AWS_SECRET_ACCESS_KEY_READ_ONLY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
logger.info(f'Storage bucket: {AWS_STORAGE_BUCKET_NAME}')
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read'
AWS_IS_GZIPPED = True

USE_LOCAL = env('USE_LOCAL', cast=bool, default=False)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
if USE_LOCAL:
    logger.info('Using local static storage')
    STATIC_URL = '/static/'

    DEFAULT_FILE_STORAGE = 'up.customStorage.OverwriteStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    logger.info('Using S3 static storage')
    AWS_LOCATION = 'static-files-dev' if IS_DEV else 'static-files'
    STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'
    logger.info(f'Static URL: {STATIC_URL}')
    STATICFILES_STORAGE = 'up.customStorage.S3ManifestStaticStorageWithLog'

    # Media file storage
    DEFAULT_FILE_STORAGE = 'up.customStorage.MediaStorage'
    MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{MEDIA_LOCATION}/'
    MEDIA_BASE = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/{MEDIA_LOCATION}/'

# Email
SENDGRID_API_KEY = env('SENDGRID_API_KEY') or os.getenv('SENDGRID_API_KEY')
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'  # Exactly that.
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587  # 25 or 587 (for unencrypted/TLS connections).
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = ('upapp.viewsAuth.EmailAuthentication',)

# SQL Logging
if env('SQL_LOG', cast=bool, default=False):
    LOGGING = {
        'version': 1,
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
            }
        }
    }
