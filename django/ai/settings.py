from common_settings import *

SECRET_KEY = 'YOUR KEY GOES HERE'

DEBUG=True

#from scheduler.models import TestTask
#SCHEDULED_TASKS = [TestTask(5, 0), ]
SCHEDULED_TASKS = []

# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ai',
        'USER': 'postgres',
        'PASSWORD': 'password_here',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
