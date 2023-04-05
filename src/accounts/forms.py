from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from accounts.models import BuyerProfile, SellerProfile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "phone_number",
            "email",
            "password1",
            "password2",
            "user_type",
        )


class SellerProfileUpdateForm(ModelForm):
    class Meta:
        model = SellerProfile
        fields = "__all__"

        exclude = ("customer", "rang")


class BuyerProfileUpdateForm(ModelForm):
    class Meta:
        model = BuyerProfile
        fields = "__all__"

        exclude = ("customer",)
