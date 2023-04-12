import re

from django_filters.views import FilterView
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
from shops.filters import ProductFilters, SellerFilters
from shops.forms import ProductCreateForm, ProductUpdateForm, OrderUpdateStatusForm
from shops.models import Order, Product
from shops.tasks import orders_generator_task, products_generator_task


class ProductsView(FilterView):
    filterset_class = ProductFilters
    template_name = "shops/products.html"


class ProductDetails(DetailView):
    queryset = Product.objects.all()
    template_name = "shops/product_details.html"
    context_object_name = "product"


class SellersView(FilterView):
    filterset_class = SellerFilters
    template_name = "shops/sellers.html"


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


class SellerNewOrderView(LoginRequiredMixin, SellerTypeRequiredMixin, ListView):
    template_name = "shops/seller_order_new.html"
    context_object_name = "orders"
    order_status = Order.StatusChoices.NEW

    def get_queryset(self):

        queryset = Order.objects.filter(status=self.order_status).filter(
            product__seller=self.request.user.seller_profile)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class SellerInWorkOrderView(SellerNewOrderView):
    template_name = "shops/seller_order_in_work.html"
    order_status = Order.StatusChoices.IN_WORK


class SellerHistoryOrderView(SellerNewOrderView):
    template_name = "shops/seller_order_history.html"
    order_status = Order.StatusChoices.EXECUTED


class SellerOrderStatusUpdateView(LoginRequiredMixin, SellerTypeRequiredMixin, UpdateView):
    template_name = "shops/seller_order_update.html"
    context_object_name = "form"
    form_class = OrderUpdateStatusForm
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.product.seller != request.user.seller_profile:
            raise PermissionDenied("No permission")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()

        kwargs["order"] = Order.objects.get(pk=self.kwargs.get("pk"))
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        _success_url = reverse_lazy("shops:seller_orders_status_update", kwargs={"pk": self.object.pk})
        return str(_success_url)


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


class BuyerOrderDetailsView(DetailView):
    template_name = "shops/buyer_order_details.html"
    queryset = Order.objects.all()
    context_object_name = "order"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.buyer != request.user.buyer_profile:
            raise PermissionDenied("No permission")

        return super().get(request, *args, **kwargs)


class BuyerOrderActiveView(LoginRequiredMixin, BuyerTypeRequiredMixin, ListView):
    template_name = "shops/buyer_order_active.html"
    context_object_name = "orders"
    order_status = [Order.StatusChoices.NEW, Order.StatusChoices.IN_WORK, ]

    def get_queryset(self):

        queryset = Order.objects.filter(status__in=self.order_status).filter(
            buyer=self.request.user.buyer_profile)

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class BuyerOrderHistoryView(BuyerOrderActiveView):
    template_name = "shops/buyer_order_history.html"
    order_status = [Order.StatusChoices.EXECUTED, ]


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


class SearchView(TemplateView):
    template_name = "shops/search.html"
    http_method_names = ["get", ]

    @use_kwargs(
        {
            'search': fields.Str(required=True, ),
        },
        location='query',
    )
    def get(self, request, *args, **kwargs):
        _context = self.get_context_data(**kwargs)

        products = Product.objects.all().filter(product_name__icontains=kwargs.get("search"))

        _context.update({"products": products})

        return self.render_to_response(_context)


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
    user_list = Product.objects.all()
    print(request.GET)
    user_filter = ProductFilters(request.GET, queryset=user_list)
    print(user_filter)
    return render(request, template_name="shops/test_view.html", context={"filter": user_filter})
