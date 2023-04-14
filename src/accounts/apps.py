from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from accounts.services.signals import create_customer_profile

        post_save.connect(create_customer_profile, sender=get_user_model())
