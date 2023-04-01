from django.http import HttpResponse
from django.shortcuts import render  # NOQA : F401
from django.views.generic import DetailView, ListView
from webargs import fields, validate
from webargs.djangoparser import use_kwargs

from accounts.models import SellerProfile
from shops.models import Product
from shops.tasks import orders_generator_task, products_generator_task


class ProductDetails(DetailView):
    queryset = Product.objects.all()
    template_name = "shops/product_details.html"
    context_object_name = "product"


class SellerDetails(DetailView):
    queryset = SellerProfile.objects.all()
    template_name = "shops/seller_details.html"
    context_object_name = "seller"


class ProductsByBrand(ListView):
    context_object_name = "products"
    template_name = "shops/product_by_brand.html"

    def get_queryset(self):
        queryset = Product.objects.all().filter(brand=self.kwargs.get("pk"))

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class ProductsByCategory(ListView):
    context_object_name = "products"
    template_name = "shops/product_by_category.html"

    def get_queryset(self):
        queryset = Product.objects.all().filter(category=self.kwargs.get("pk"))

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


@use_kwargs(
    {
        'count': fields.Int(required=True, validate=[validate.Range(min=1, max=100)]),
    },
    location='query',
)
def generate_products_view(request, count):
    products_generator_task.delay(count)
    return HttpResponse('Task is started')


@use_kwargs(
    {
        'count': fields.Int(required=True, validate=[validate.Range(min=1, max=100)]),
    },
    location='query',
)
def generate_orders_view(request, count):
    orders_generator_task.delay(count)
    return HttpResponse('Task is started')
