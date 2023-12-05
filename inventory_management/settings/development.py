from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '', # Replace your DB name here
        'USER': '', # Replace your DB user here
        'PASSWORD': '', # Replace your DB password here
        'HOST': 'localhost',
        'PORT': '5433',
    }
}