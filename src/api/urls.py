from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views import (BrandCreateView, BrandDeleteView, BrandRetrieveView,
                       BrandUpdateView, CategoryCreateView, CategoryDeleteView,
                       CategoryRetrieveView, CategoryUpdateView,
                       CustomerCreateView, CustomerDeleteView, CustomerProfile,
                       CustomerProfileUpdate, CustomerRetrieveView,
                       CustomersListView, CustomerUpdateView, OrderCreateView,
                       OrderDeleteView, OrderListView, OrderRetrieveView,
                       OrderUpdateView, ProductCreateView, ProductDeleteView,
                       ProductListView, ProductParameterCreateView,
                       ProductParameterDeleteView,
                       ProductParameterRetrieveView,
                       ProductParameterUpdateView, ProductRetrieveView,
                       ProductUpdateView, RequestCreateView, RequestDeleteView,
                       RequestRetrieveView, RequestUpdateView,
                       TenderCreateView, TenderDeleteView, TenderRetrieveView,
                       TenderUpdateView)

app_name = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="MyMarker API",
        default_version="v1",
        description="API for my magazine",
        term_of_service="https://www.myterms.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="swagger_docs"),
    path("customers/", CustomersListView.as_view(), name="all_customers"),
    path("customers/<int:pk>/", CustomerRetrieveView.as_view(), name="customer_detail"),
    path("customers/create/", CustomerCreateView.as_view(), name='customer_create'),
    path("customers/update/<int:pk>/", CustomerUpdateView.as_view(), name="customer_update"),
    path("customers/delete/<int:pk>/", CustomerDeleteView.as_view(), name="customer_delete"),
    path("customers/<int:customer_id>/profile/", CustomerProfile.as_view(), name="customer_profile"),
    path(
        "customers/<int:customer_id>/profile/update/", CustomerProfileUpdate.as_view(), name="customer_profile_update"
    ),
    path("products/", ProductListView.as_view(), name="all_products"),
    path("products/<int:pk>/", ProductRetrieveView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("products/delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("orders/", OrderListView.as_view(), name="all_order"),
    path("orders/<int:pk>/", OrderRetrieveView.as_view(), name="order_detail"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/update/<int:pk>/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/delete/<int:pk>/", OrderDeleteView.as_view(), name="order_delete"),
    path("category/<int:pk>/", CategoryRetrieveView.as_view(), name="category_detail"),
    path("category/create/", CategoryCreateView.as_view(), name="category_create"),
    path("category/update/<int:pk>/", CategoryUpdateView.as_view(), name="category_update"),
    path("category/delete/<int:pk>/", CategoryDeleteView.as_view(), name="category_delete"),
    path("brands/<int:pk>/", BrandRetrieveView.as_view(), name="brand_detail"),
    path("brands/create/", BrandCreateView.as_view(), name="brand_create"),
    path("brands/update/<int:pk>/", BrandUpdateView.as_view(), name="brand_update"),
    path("brands/delete/<int:pk>/", BrandDeleteView.as_view(), name="brand_delete"),
    path("tenders/<int:pk>/", TenderRetrieveView.as_view(), name="tender_detail"),
    path("tenders/create/", TenderCreateView.as_view(), name="tender_create"),
    path("tenders/update/<int:pk>/", TenderUpdateView.as_view(), name="tender_update"),
    path("tenders/delete/<int:pk>/", TenderDeleteView.as_view(), name="tender_delete"),
    path("products-parameter/<int:pk>/", ProductParameterRetrieveView.as_view(), name="product_parameter_detail"),
    path("products-parameter/create/", ProductParameterCreateView.as_view(), name="product_parameter_create"),
    path("products-parameter/update/<int:pk>/", ProductParameterUpdateView.as_view(), name="product_parameter_update"),
    path("products-parameter/delete/<int:pk>/", ProductParameterDeleteView.as_view(), name="product_parameter_delete"),
    path("requests/<int:pk>/", RequestRetrieveView.as_view(), name="request_detail"),
    path("requests/create/", RequestCreateView.as_view(), name="request_create"),
    path("requests/update/<int:pk>/", RequestUpdateView.as_view(), name="request_update"),
    path("requests/delete/<int:pk>/", RequestDeleteView.as_view(), name="request_delete"),
]
