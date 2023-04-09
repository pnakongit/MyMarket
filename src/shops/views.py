import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render  # NOQA : F401
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)
from webargs import fields, validate
from webargs.djangoparser import use_kwargs

from accounts.models import SellerProfile
from core.permissions import BuyerTypeRequiredMixin, SellerTypeRequiredMixin
from core.utils.helpers import (add_shopping_cart_information_to_session,
                                get_shopping_cart_data)
from shops.forms import ArticleFormSet, ProductCreateForm, ProductUpdateForm
from shops.models import Order, Product
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

        if shopping_cart:
            shopping_cart_data = get_shopping_cart_data(request)

            context.update(**shopping_cart_data)

        return self.render_to_response(context)


class ShoppingCartAddProductRedirect(View):
    def get(self, request, *args, **kwargs):
        product_pk = kwargs.get("pk")
        quantity = kwargs.get("quantity")
        if all([product_pk, quantity]):
            add_shopping_cart_information_to_session(request, product_pk=product_pk, quantity=quantity)
        return HttpResponseRedirect(reverse_lazy("shops:shopping_cart"))


class ShoppingCartUpdateProductRedirectPost(View):
    http_method_names = [
        'post',
    ]

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if re.match(r"^product_", key):
                add_shopping_cart_information_to_session(request, product_pk=key[8:], quantity=value)

        if "check_out" in request.POST:
            return HttpResponseRedirect(reverse_lazy("shops:check_out"))

        if "update" in request.POST:
            return HttpResponseRedirect(reverse_lazy("shops:shopping_cart"))

        return HttpResponseRedirect(reverse_lazy("shops:index"))


class ShoppingCartDeleteProductRedirect(View):
    def get(self, request, *args, **kwargs):
        product_pk = kwargs.get("pk")

        add_shopping_cart_information_to_session(request, product_pk=product_pk, delete=True)
        return HttpResponseRedirect(reverse_lazy("shops:shopping_cart"))


class CheckOutView(LoginRequiredMixin, BuyerTypeRequiredMixin, ShoppingCart):
    template_name = "shops/check_out.html"


class OrderCreatePostView(LoginRequiredMixin, BuyerTypeRequiredMixin, View):
    http_method_names = [
        'post',
    ]

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if re.match(r"^product_", key):
                product = Product.objects.get(pk=key[8:])
                new_order = Order()
                new_order.product = product
                new_order.amount = value
                new_order.buyer = request.user.buyer_profile
                new_order.save()
        del request.session["shopping_cart"]

        return HttpResponseRedirect(reverse_lazy("shops:index"))


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


def my_test_view(request, *args, **kwargs):
    print(request.POST)

    formset = ArticleFormSet()
    if request.POST:
        formset = ArticleFormSet(request.POST)
        print(formset.total_form_count())

    return render(request, template_name="shops/test_view.html", context={"formset": formset})
