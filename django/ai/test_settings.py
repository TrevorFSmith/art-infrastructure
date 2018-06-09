from settings import *

SECRET_KEY = 'YOUR KEY GOES HERE'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

#from scheduler import TestTask
#SCHEDULED_TASKS = [TestTask(5, 0), ]
SCHEDULED_TASKS = []

# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ai_test',
        'USER': 'postgres',
        'PASSWORD': 'password_here',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

MEDIA_ROOT = os.path.realpath(os.path.join(BASE_DIR, '..', 'media/for_test'))
