from django.shortcuts import render  # NOQA : F401
from django.views.generic import DetailView

from accounts.models import SellerProfile
from shops.models import Product


class ProductDetails(DetailView):
    queryset = Product.objects.all()
    template_name = "shops/product_details.html"
    context_object_name = "product"


class SellerDetails(DetailView):
    queryset = SellerProfile.objects.all()
    template_name = "shops/seller_details.html"
    context_object_name = "seller"
