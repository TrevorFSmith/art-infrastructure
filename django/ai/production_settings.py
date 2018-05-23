from settings import *

# FIXME: replace with real key
SECRET_KEY = "YOUR KEY GOES HERE"

# FIXME: replace with real password
IBOOT_POWER_PASSWORD=""

DEBUG=False

#from scheduler import TestTask
#SCHEDULED_TASKS = [TestTask(5, 0), ]
SCHEDULED_TASKS = []

# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ai',
        'USER': 'postgres',
        'PASSWORD': 'mooa',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
