from django import forms
from django.forms import ModelForm, formset_factory

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
