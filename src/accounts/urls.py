from django.urls import path

from accounts.views import generate_accounts_view

app_name = 'accounts'

urlpatterns = [
    path("generate/", generate_accounts_view, name="generate_test_account"),
]
