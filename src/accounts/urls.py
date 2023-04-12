from django.urls import path

from accounts.views import (BuyerProfileUpdateView, BuyerProfileView,
                            SellerProfileUpdateView, SellerProfileView,
                            UserLoginView, UserLogoutView,
                            UserRegistrationView, generate_accounts_view)

app_name = 'accounts'

urlpatterns = [
    path("generate/", generate_accounts_view, name="generate_test_account"),
    path("registration/", UserRegistrationView.as_view(), name='registration'),
    path("login/", UserLoginView.as_view(), name='login'),
    path("logout/", UserLogoutView.as_view(), name='logout'),
    path("seller-profile/", SellerProfileView.as_view(), name="seller_profile"),
    path("seller-profile/update/", SellerProfileUpdateView.as_view(), name="seller_profile_update"),
    path("buyer-profile/", BuyerProfileView.as_view(), name="buyer_profile"),
    path("buyer-profile/update/", BuyerProfileUpdateView.as_view(), name="buyer_profile_update"),
]
