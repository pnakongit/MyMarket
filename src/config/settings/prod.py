import os

from config.settings.base import *  # NOQA

DEBUG = False

SECRET_KEY = "django-insecure-s4hy4e0bscfl)objduu9@*!889_7ewf$e!)ganyn!r(zx(me$*"

ALLOWED_HOSTS = ["localhost"]

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR.parent / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'media'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("POSTGRES_PORT"),
    },
}
