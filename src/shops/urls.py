from django.urls import path

from core.views import IndexView
from shops.views import (CheckOutView, OrderCreatePostView, ProductCreateView,
                         ProductDeleteView, ProductDetails, ProductsByBrand,
                         ProductsByCategory, ProductUpdateView, SellerDetails,
                         SellerProductView, ShoppingCart,
                         ShoppingCartAddProductRedirect,
                         ShoppingCartDeleteProductRedirect,
                         ShoppingCartUpdateProductRedirectPost,
                         generate_orders_view, generate_products_view,
                         my_test_view, ProductsView, SellersView, SearchView, SellerNewOrderView,
                         SellerOrderStatusUpdateView, SellerInWorkOrderView, SellerHistoryOrderView,
                         BuyerOrderActiveView, BuyerOrderHistoryView, BuyerOrderDetailsView)

app_name = 'shops'

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path("products/", ProductsView.as_view(), name="products"),
    path("products/<int:pk>/", ProductDetails.as_view(), name="product_details"),
    path("products/brand/<int:pk>/", ProductsByBrand.as_view(), name="products_by_brand"),
    path("products/category/<int:pk>/", ProductsByCategory.as_view(), name="products_by_category"),
    path("shopping-cart/", ShoppingCart.as_view(), name="shopping_cart"),
    path("shopping-cart/update/", ShoppingCartUpdateProductRedirectPost.as_view(), name="shopping_cart_update_post"),
    path(
        "shopping-cart/add/<int:pk>/quantity/<int:quantity>",
        ShoppingCartAddProductRedirect.as_view(),
        name="shopping_cart_add",
    ),
    path("shopping-cart/delete/<int:pk>/", ShoppingCartDeleteProductRedirect.as_view(), name="shopping_cart_delete"),
    path("check-out/", CheckOutView.as_view(), name="check_out"),
    path("order/create/", OrderCreatePostView.as_view(), name="order_create_post_view"),
    path("sellers/", SellersView.as_view(), name="sellers"),
    path("sellers/<int:pk>", SellerDetails.as_view(), name="seller_details"),
    path("generate-products/", generate_products_view, name="generate_products"),
    path("generate-orders/", generate_orders_view, name="generate_orders"),
    path("my-seller/products/", SellerProductView.as_view(), name="seller_product_all"),
    path("my-seller/products/create/", ProductCreateView.as_view(), name="seller_product_create"),
    path("my-seller/products/update/<int:pk>/", ProductUpdateView.as_view(), name="seller_product_update"),
    path("my-seller/products/delete/<int:pk>/", ProductDeleteView.as_view(), name="seller_product_delete"),
    path("my-seller/orders/new/", SellerNewOrderView.as_view(), name="seller_orders_new"),
    path("my-seller/orders/in-work/", SellerInWorkOrderView.as_view(), name="seller_orders_in_work"),
    path("my-seller/orders/history/", SellerHistoryOrderView.as_view(), name="seller_orders_history"),
    path("my-seller/orders/status-update/<int:pk>/", SellerOrderStatusUpdateView.as_view(),
         name="seller_orders_status_update"),
    path("my-buyer/orders/<int:pk>/", BuyerOrderDetailsView.as_view(), name="buyer_orders_details"),
    path("my-buyer/orders/active/", BuyerOrderActiveView.as_view(), name="buyer_orders_active"),
    path("my-buyer/orders/history/", BuyerOrderHistoryView.as_view(), name="buyer_orders_history"),
    path("search/", SearchView.as_view(), name="search"),
    path("test/", my_test_view, name="my_test_view"),
]
