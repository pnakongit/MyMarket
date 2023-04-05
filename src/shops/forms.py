from django.forms import ModelForm

from shops.models import Product


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("available", "seller")


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ("seller",)
