from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from accounts.models import BuyerProfile, SellerProfile
from shops.models import Brand, Category, Order, Product
from tenders.models import ProductParameter, Request, Tender


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ["password"]
        read_only_fields = ["user_type"]


class CustomerCreateSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "phone_number", "password", "user_type")


class BuyerProfileSerializer(ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = '__all__'
        read_only_fields = ["customer_id"]


class SellerProfileSerializer(ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = '__all__'
        read_only_fields = ["customer_id"]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class TenderSerializer(ModelSerializer):
    class Meta:
        model = Tender
        fields = '__all__'


class ProductParameterSerializer(ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = '__all__'


class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
