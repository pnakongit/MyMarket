from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DetailView, UpdateView
from webargs import fields, validate
from webargs.djangoparser import use_kwargs

from accounts.forms import (BuyerProfileUpdateForm, SellerProfileUpdateForm,
                            UserRegistrationForm)
from accounts.models import BuyerProfile, SellerProfile
from accounts.tasks import accounts_generator_task
from core.permissions import BuyerTypeRequiredMixin, SellerTypeRequiredMixin


@use_kwargs(
    {
        'count': fields.Int(required=True, validate=[validate.Range(min=1, max=100)]),
        'user_type': fields.Int(required=True, validate=[validate.Range(min=0, max=1)]),
    },
    location='query',
)
def generate_accounts_view(request, count, user_type):
    accounts_generator_task.delay(count=count, user_type=user_type)

    return HttpResponse("Task is started")


class UserRegistrationView(CreateView):
    template_name = "accounts/registration/registration.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)

        if self.object.user_type == get_user_model().TypeChoices.BUYER:
            return HttpResponseRedirect(reverse_lazy("accounts:buyer_profile_update"))

        return HttpResponseRedirect(reverse_lazy("accounts:seller_profile_update"))


class UserLoginView(LoginView):
    template_name = "accounts/registration/login.html"
    next_page = reverse_lazy("shops:index")
    redirect_authenticated_user = True


class UserLogoutView(LoginRequiredMixin, LogoutView):
    ...


class CustomObjectGet:
    profile_model = ""

    def get_object(self, queryset=None):
        try:
            obj = self.profile_model.objects.get(customer=self.request.user)
        except queryset.model.DoesNotExist:
            raise Http404(_("No  found matching the query"))
        return obj


class BuyerProfileView(LoginRequiredMixin, BuyerTypeRequiredMixin, CustomObjectGet, DetailView):
    profile_model = BuyerProfile
    context_object_name = "buyer"
    form_class = BuyerProfileUpdateForm
    template_name = "accounts/buyer_profile.html"


class BuyerProfileUpdateView(LoginRequiredMixin, BuyerTypeRequiredMixin, CustomObjectGet, UpdateView):
    context_object_name = "form"
    form_class = BuyerProfileUpdateForm
    success_url = reverse_lazy("accounts:buyer_profile")
    template_name = "accounts/buyer_profile_update.html"
    profile_model = BuyerProfile


class SellerProfileView(LoginRequiredMixin, SellerTypeRequiredMixin, CustomObjectGet, DetailView):
    context_object_name = "seller"
    form_class = SellerProfileUpdateForm
    template_name = "accounts/seller_profile.html"
    profile_model = SellerProfile


class SellerProfileUpdateView(LoginRequiredMixin, SellerTypeRequiredMixin, CustomObjectGet, UpdateView):
    context_object_name = "form"
    form_class = SellerProfileUpdateForm
    success_url = reverse_lazy("accounts:seller_profile")
    template_name = "accounts/seller_profile_update.html"
    profile_model = SellerProfile
