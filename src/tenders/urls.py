from django.urls import path

from tenders.views import (BuyerTenderDetailsView, BuyerTendersView,
                           TenderAddProductParameterView, TenderCreateView,
                           TenderDetailsView, TenderStatusUpdatePostView,
                           TendersView)

app_name = 'tenders'

urlpatterns = [
    path("", TendersView.as_view(), name="all_tender"),
    path("details/<int:pk>/", TenderDetailsView.as_view(), name="tender_details"),
    path("my-buyer/", BuyerTendersView.as_view(), name="buyer_account_all_tender"),
    path("create/", TenderCreateView.as_view(), name="tender_create"),
    path("my-buyer/details/<int:pk>/", BuyerTenderDetailsView.as_view(), name="buyer_tender_details"),
    path(
        "my-buyer/details/<int:pk>/add-product-parameter/",
        TenderAddProductParameterView.as_view(),
        name="tender_add_product_parameter",
    ),
    path("my-buyer/details/<int:pk>/update/", TenderStatusUpdatePostView.as_view(), name="tender_status_update"),
]
