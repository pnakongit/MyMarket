from django.urls import path

from shops.views import (ProductDetails, ProductsByBrand, ProductsByCategory,
                         SellerDetails, generate_orders_view,
                         generate_products_view)

app_name = 'shops'

urlpatterns = [
    path("product/<int:pk>", ProductDetails.as_view(), name="product_details"),
    path("products-by-brand/<int:pk>/", ProductsByBrand.as_view(), name="products_by_brand"),
    path("products-by-category/<int:pk>/", ProductsByCategory.as_view(), name="products_by_category"),
    path("seller/<int:pk>", SellerDetails.as_view(), name="seller_details"),
    path("generate-products/", generate_products_view, name="generate_products"),
    path("generate-orders/", generate_orders_view, name="generate_orders"),
]
