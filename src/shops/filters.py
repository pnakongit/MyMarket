from django import forms
from django_filters import FilterSet, ModelMultipleChoiceFilter, NumberFilter

from accounts.models import SellerProfile
from shops.models import Brand, Category, Product


class ProductFilters(FilterSet):
    brand = ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)

    category = ModelMultipleChoiceFilter(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    price__gt = NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = [
            "brand",
            "category",
        ]


class SellerFilters(FilterSet):
    product__brand = ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)

    product__category = ModelMultipleChoiceFilter(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = SellerProfile
        fields = {
            "brand_name": [
                "icontains",
            ]
        }
