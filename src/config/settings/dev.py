import os

from config.settings.base import *  # NOQA

DEBUG = True

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = []

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": 5432,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
        'default_postgresql': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get("POSTGRES_DB"),
            'USER': os.environ.get("POSTGRES_USER"),
            'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
            'HOST': os.environ.get("POSTGRES_HOST"),
            'PORT': os.environ.get("POSTGRES_PORT"),
        },
        'default_nongo': {
            'ENGINE': 'djongo',
            'NAME': os.environ.get('MONGO_INITDB_DATABASE'),
            'CLIENT': {
                'host': 'mongodb://mongodb:27017',
                'username': os.environ.get('MONGO_INITDB_ROOT_USERNAME'),
                'password': os.environ.get('MONGO_INITDB_ROOT_PASSWORD'),
                'authSource': 'admin',
                'authMechanism': 'SCRAM-SHA-1',
            },
        },
    }
