from rest_framework.permissions import BasePermission


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == 0:
            return True

        return False


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == 1:
            return True

        return False
