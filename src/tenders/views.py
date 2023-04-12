from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render  # NOQA : F401
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from django_filters.views import FilterView

from core.permissions import BuyerTypeRequiredMixin
from tenders.filters import TendersBuyerFilter, TendersFilter
from tenders.forms import CreateProductParameterForm, TenderCreateForm
from tenders.models import Tender


class TenderCreateView(LoginRequiredMixin, BuyerTypeRequiredMixin, CreateView):
    template_name = "tenders/create_tender.html"
    form_class = TenderCreateForm
    context_object_name = "form"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.buyer = self.request.user.buyer_profile
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        _success_url = reverse_lazy("tenders:buyer_tender_details", kwargs={"pk": self.object.pk})
        return str(_success_url)


class BuyerTenderDetailsView(LoginRequiredMixin, BuyerTypeRequiredMixin, TemplateView):
    template_name = "tenders/buyer_tender_details.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        tender = get_object_or_404(Tender, pk=kwargs.get("pk"))

        if tender.buyer != request.user.buyer_profile:
            raise PermissionDenied()

        context["tender"] = tender

        return self.render_to_response(context)


class TenderAddProductParameterView(LoginRequiredMixin, BuyerTypeRequiredMixin, CreateView):
    template_name = "tenders/tender_add_product_parameter.html"
    form_class = CreateProductParameterForm
    context_object_name = "form"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.tender = get_object_or_404(Tender, pk=self.kwargs.get("pk"))
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        _success_url = reverse_lazy("tenders:buyer_tender_details", kwargs={"pk": self.object.tender.pk})
        return str(_success_url)


class TenderStatusUpdatePostView(LoginRequiredMixin, BuyerTypeRequiredMixin, View):
    http_method_names = [
        "post",
    ]

    def post(self, request, *args, **kwargs):
        tender = get_object_or_404(Tender, pk=kwargs.get("pk"))
        if tender.buyer != request.user.buyer_profile:
            raise PermissionDenied()

        if "publish_a_tender" in request.POST:
            tender.status = Tender.StatusChoices.PUBLISHED
            tender.save()

        elif "cancel" in request.POST:
            tender.status = Tender.StatusChoices.CANCELED
            tender.save()

        _success_url = reverse_lazy("tenders:buyer_tender_details", kwargs={"pk": tender.pk})
        return HttpResponseRedirect(_success_url)


class BuyerTendersView(FilterView):
    template_name = "tenders/buyer_tenders.html"
    filterset_class = TendersBuyerFilter


class TendersView(FilterView):
    template_name = "tenders/tenders.html"
    filterset_class = TendersFilter


class TenderDetailsView(TemplateView):
    template_name = "tenders/tender_details.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        tender = get_object_or_404(Tender, pk=kwargs.get("pk"))

        if tender.status != Tender.StatusChoices.PUBLISHED:
            return HttpResponseRedirect(reverse_lazy("tenders:all_tender"))

        context["tender"] = tender

        return self.render_to_response(context)
