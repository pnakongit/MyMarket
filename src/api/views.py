from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)

from accounts.models import BuyerProfile, SellerProfile
from api.serializers import (BrandSerializer, BuyerProfileSerializer,
                             CategorySerializer, CustomerCreateSerializer,
                             CustomerSerializer, OrderSerializer,
                             ProductParameterSerializer, ProductSerializer,
                             RequestSerializer, SellerProfileSerializer,
                             TenderSerializer)
from core.permissions import IsBuyer, IsSeller
from shops.models import Brand, Category, Order, Product
from tenders.models import ProductParameter, Request, Tender


class CustomersListView(ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class CustomerRetrieveView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class CustomerCreateView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerCreateSerializer


class CustomerUpdateView(UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerSerializer


class CustomerDeleteView(DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomerCreateSerializer


class CustomerProfile(RetrieveAPIView):
    lookup_field = "customer_id"

    def get_queryset(self):
        customer = get_object_or_404(get_user_model(), pk=self.kwargs.get('customer_id'))

        if customer.user_type == 0:
            queryset = BuyerProfile.objects.all()
        elif customer.user_type == 1:
            queryset = SellerProfile.objects.all()
        else:
            raise Http404("No profile")
        return queryset

    def get_serializer_class(self):
        customer = get_object_or_404(get_user_model(), pk=self.kwargs.get('customer_id'))
        if customer.user_type == 0:
            self.serializer_class = BuyerProfileSerializer
        elif customer.user_type == 1:
            self.serializer_class = SellerProfileSerializer
        else:
            raise Http404("No profile")
        return self.serializer_class


class CustomerProfileUpdate(UpdateAPIView):
    lookup_field = "customer_id"

    def get_queryset(self):
        customer = get_object_or_404(get_user_model(), pk=self.kwargs.get('customer_id'))

        if customer.user_type == 0:
            queryset = BuyerProfile.objects.all()
        elif customer.user_type == 1:
            queryset = SellerProfile.objects.all()
        else:
            raise Http404("No profile")
        return queryset

    def get_serializer_class(self):
        customer = get_object_or_404(get_user_model(), pk=self.kwargs.get('customer_id'))
        if customer.user_type == 0:
            self.serializer_class = BuyerProfileSerializer
        elif customer.user_type == 1:
            self.serializer_class = SellerProfileSerializer
        else:
            raise Http404("No profile")
        return self.serializer_class


class ProductListView(ListAPIView):
    permission_classes = [IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveView(RetrieveAPIView):
    permission_classes = [IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(CreateAPIView):
    permission_classes = [IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateView(UpdateAPIView):
    permission_classes = [IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDeleteView(DestroyAPIView):
    permission_classes = [IsSeller]
    queryset = Product.objects.all()


class OrderListView(ListAPIView):
    permission_classes = [IsBuyer]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRetrieveView(RetrieveAPIView):
    permission_classes = [IsBuyer]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderCreateView(CreateAPIView):
    permission_classes = [IsBuyer]
    serializer_class = OrderSerializer


class OrderUpdateView(UpdateAPIView):
    permission_classes = [IsBuyer]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDeleteView(DestroyAPIView):
    permission_classes = [IsBuyer]
    queryset = Order.objects.all()


class CategoryRetrieveView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(CreateAPIView):
    serializer_class = CategorySerializer


class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()


class BrandRetrieveView(RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandCreateView(CreateAPIView):
    serializer_class = BrandSerializer


class BrandUpdateView(UpdateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDeleteView(DestroyAPIView):
    queryset = Brand.objects.all()


class TenderRetrieveView(RetrieveAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer


class TenderCreateView(CreateAPIView):
    serializer_class = TenderSerializer


class TenderUpdateView(UpdateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer


class TenderDeleteView(DestroyAPIView):
    queryset = Tender.objects.all()


class ProductParameterRetrieveView(RetrieveAPIView):
    queryset = ProductParameter.objects.all()
    serializer_class = ProductParameterSerializer


class ProductParameterCreateView(CreateAPIView):
    serializer_class = ProductParameterSerializer


class ProductParameterUpdateView(UpdateAPIView):
    queryset = ProductParameter.objects.all()
    serializer_class = ProductParameterSerializer


class ProductParameterDeleteView(DestroyAPIView):
    queryset = ProductParameter.objects.all()


class RequestRetrieveView(RetrieveAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class RequestCreateView(CreateAPIView):
    serializer_class = RequestSerializer


class RequestUpdateView(UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class RequestDeleteView(DestroyAPIView):
    queryset = Request.objects.all()
