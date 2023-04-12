from django.forms import ModelForm

from shops.models import Product, Order


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


class OrderUpdateStatusForm(ModelForm):
    class Meta:
        model = Order
        fields = ("status",)
