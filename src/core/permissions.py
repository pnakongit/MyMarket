from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework.permissions import BasePermission


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == get_user_model().TypeChoices.BUYER:
            return True

        return False


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == get_user_model().TypeChoices.SELLER:
            return True

        return False


class SellerTypeRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.user_type == get_user_model().TypeChoices.SELLER:
            return True

        return False


class BuyerTypeRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.user_type == get_user_model().TypeChoices.BUYER:
            return True

        return False
