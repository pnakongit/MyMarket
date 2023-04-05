from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomerManager
from accounts.utils.validators import brand_name_unique_validator


class Customer(AbstractBaseUser, PermissionsMixin):
    class TypeChoices(models.IntegerChoices):
        BUYER = 0, "Buyer"
        SELLER = 1, "Seller"

    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    user_type = models.PositiveIntegerField(choices=TypeChoices.choices, default=TypeChoices.BUYER)

    objects = CustomerManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @staticmethod
    def get_all_buyers():
        return Customer.objects.filter(user_type=0)

    @staticmethod
    def get_all_seller():
        return Customer.objects.filter(user_type=1)

    def __str__(self):
        return f"{self.email} - {self.user_type}"


class BuyerProfile(models.Model):
    customer = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="buyer_profile")
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    birthdate = models.DateField(_("day of birth"), blank=True, null=True)
    avatar = models.ImageField(upload_to='accounts/uploads/', null=True, blank=True)

    def __str__(self):
        return f"{self.pk} {self.first_name} {self.last_name}"


class SellerProfile(models.Model):
    customer = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="seller_profile")
    brand_name = models.CharField(_("brand name"), max_length=150, validators=[brand_name_unique_validator])
    description = models.CharField(_("short description"), max_length=300, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    location = PlainLocationField(based_fields=['city'], zoom=7, blank=True, null=True)
    url = models.URLField(unique=True, blank=True, null=True, max_length=250)
    rang = models.PositiveIntegerField(blank=True, null=True)
    logo = models.ImageField(upload_to='accounts/uploads/', null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.brand_name}"
