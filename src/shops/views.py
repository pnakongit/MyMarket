from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render  # NOQA : F401
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from webargs import fields, validate
from webargs.djangoparser import use_kwargs

from accounts.models import SellerProfile
from core.permissions import SellerTypeRequiredMixin
from shops.forms import ProductCreateForm, ProductUpdateForm
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


class SellerProductView(LoginRequiredMixin, SellerTypeRequiredMixin, ListView):
    context_object_name = "products"
    template_name = "shops/my_seller_product.html"

    def get_queryset(self):
        _seller_profile = self.request.user.seller_profile
        queryset = Product.objects.all().filter(seller=_seller_profile)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class ProductCreateView(LoginRequiredMixin, SellerTypeRequiredMixin, CreateView):
    context_object_name = "form"
    form_class = ProductCreateForm
    template_name = "shops/product_create.html"
    success_url = reverse_lazy("shops:seller_product_all")
    model = Product

    def form_valid(self, form):
        product = form.save()
        product.seller = self.request.user.seller_profile
        self.object = product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, SellerTypeRequiredMixin, UpdateView):
    template_name = "shops/product_update.html"
    form_class = ProductUpdateForm
    queryset = Product.objects.all()
    success_url = reverse_lazy("shops:seller_product_all")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.seller != request.user.seller_profile:
            raise PermissionDenied("No permission")

        return super().get(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, SellerTypeRequiredMixin, DeleteView):
    queryset = Product.objects.all()
    success_url = reverse_lazy("shops:seller_product_all")
    template_name = "shops/product_delete_confirm.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.seller != request.user.seller_profile:
            raise PermissionDenied("No permission")

        return super().get(request, *args, **kwargs)


class ShoppingCart(TemplateView):
    template_name = "shops/shopping_cart.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        shopping_cart = request.session.get("shopping_cart", None)
        print(shopping_cart)

        if shopping_cart:
            or_filter = Q()
            for product in shopping_cart:
                or_filter |= Q(pk=product)

            products = Product.objects.filter(or_filter)

            shopping_cart_data = {}
            total_price = 0

            for product in products:
                total_price_of_product = product.price * shopping_cart.get(f"{product.pk}")
                shopping_cart_data.update(
                    {
                        product.pk: {
                            "product_name": product.product_name,
                            "product_price": product.price,
                            "count": shopping_cart.get(f"{product.pk}"),
                            "total_price_of_product": total_price_of_product,
                            "seller": product.seller.brand_name,
                            "url": product.image.url if product.image else "",
                        }
                    }
                )
                total_price += total_price_of_product

            context.update({"shopping_cart_data": shopping_cart_data, "total_price": total_price})

        return self.render_to_response(context)


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
