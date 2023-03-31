from django.urls import path

from shops.views import (ProductDetails, SellerDetails, generate_orders_view,
                         generate_products_view)

app_name = 'shops'

urlpatterns = [
    path("product/<int:pk>", ProductDetails.as_view(), name="product_details"),
    path("seller/<int:pk>", SellerDetails.as_view(), name="seller_details"),
    path("generate-products/", generate_products_view, name="generate_products"),
    path("generate-orders/", generate_orders_view, name="generate_orders"),
]
