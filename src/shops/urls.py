from django.urls import path

from shops.views import ProductDetails, SellerDetails

app_name = 'shops'

urlpatterns = [
    path("product/<int:pk>", ProductDetails.as_view(), name="product_details"),
    path("seller/<int:pk>", SellerDetails.as_view(), name="seller_details"),
]
