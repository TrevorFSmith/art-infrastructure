import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

DEBUG=False

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'

BACNET_BIN_DIR = "./"

SITE_ID = 1

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'), )

COMPRESS_ROOT = STATIC_ROOT = os.path.realpath(os.path.join(BASE_DIR, '..', 'static'))
COMPRESS_ENABLED = not DEBUG

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',

    'rest_framework',
    'rest_framework.authtoken',
    'django_nose',

    'scheduler',
    'front',
    'account',
    'artwork',
    'heartbeat',
    'lighting',
    'weather',
    'iboot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'ai/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ai.context_processors.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai.wsgi.application'

SASS_COMMAND = 'sass --scss {infile} {outfile}'

COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/x-scss', SASS_COMMAND),
)

# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = []

USE_I18N = True
USE_L10N = True
USE_TZ = True

PRODUCTION = False
DEBUG = True

ALLOWED_HOSTS = []
