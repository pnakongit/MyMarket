from config.settings.base import *  # NOQA

DEBUG = False

SECRET_KEY = "django-insecure-s4hy4e0bscfl)objduu9@*!889_7ewf$e!)ganyn!r(zx(me$*"

ALLOWED_HOSTS = []

STATIC_URL = "static/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
