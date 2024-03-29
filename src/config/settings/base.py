"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "phonenumber_field",
    "location_field.apps.DefaultConfig",
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_celery_beat",
    "drf_yasg",
    "djoser",
    "djmoney",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_inlinecss",
    "accounts",
    "core",
    "shops",
    "tenders",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

LOGIN_REDIRECT_URL = "accounts:index"
LOGOUT_REDIRECT_URL = "accounts:login"
LOGIN_URL = "accounts:login"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.all_categories_context_processors",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

AUTH_USER_MODEL = "accounts.Customer"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=100),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "PASSWORD_RESET_CONFIRM_URL": "auth/password-reset/{uid}/{token}",
}

CELERY_BROKER_URL = "redis://redis"
CELERY_BROKER_BACKEND = "redis://redis"

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

CELERY_BEAT_SCHEDULE = {
    "some_periodic_task": {"task": "accounts.tasks.test_task", "schedule": crontab(minute="*/15")},
    "at_12_00_on_friday": {
        "task": "accounts.tasks.test_task",
        "schedule": crontab(minute="0", hour="12", day_of_month="*", month_of_year="*", day_of_week="5"),
    },
    "my_birth_day": {
        "task": "accounts.tasks.test_task",
        "schedule": crontab(minute="4", hour="5", day_of_month="3", month_of_year="9"),
    },
    "tender_status_change": {
        "task": "tenders.tasks.tender_status_change_task",
        "schedule": crontab(minute="0", hour="0", day_of_month="*", month_of_year="*", day_of_week="*"),
    },
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = False
