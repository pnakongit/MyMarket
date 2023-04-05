from django.urls import path

from core.views import IndexView
from shops.views import (ProductCreateView, ProductDeleteView, ProductDetails,
                         ProductsByBrand, ProductsByCategory,
                         ProductUpdateView, SellerDetails, SellerProductView,
                         ShoppingCart, generate_orders_view,
                         generate_products_view)

app_name = 'shops'

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path("product/<int:pk>", ProductDetails.as_view(), name="product_details"),
    path("products-by-brand/<int:pk>/", ProductsByBrand.as_view(), name="products_by_brand"),
    path("products-by-category/<int:pk>/", ProductsByCategory.as_view(), name="products_by_category"),
    path("shopping-cart", ShoppingCart.as_view(), name="shopping_cart"),
    path("seller/<int:pk>", SellerDetails.as_view(), name="seller_details"),
    path("generate-products/", generate_products_view, name="generate_products"),
    path("generate-orders/", generate_orders_view, name="generate_orders"),
    path("my-seller/product/", SellerProductView.as_view(), name="seller_product_all"),
    path("my-seller/product/create/", ProductCreateView.as_view(), name="seller_product_create"),
    path("my-seller/product/update/<int:pk>", ProductUpdateView.as_view(), name="seller_product_update"),
    path("my-seller/product/delete/<int:pk>", ProductDeleteView.as_view(), name="seller_product_delete"),
]
