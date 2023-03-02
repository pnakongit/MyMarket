from django.core.exceptions import ValidationError


def brand_name_unique_validator(brand_name):
    from accounts.models import SellerProfile

    if SellerProfile.objects.filter(brand_name=brand_name).exists():
        raise ValidationError("Customer with brand name already exists!!!")
