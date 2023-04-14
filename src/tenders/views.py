from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render  # NOQA : F401
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from django_filters.views import FilterView

from core.permissions import BuyerTypeRequiredMixin, SellerTypeRequiredMixin
from tenders.filters import (TendersBuyerFilter, TendersFilter,
                             TendersSellerFilter)
from tenders.forms import CreateProductParameterForm, TenderCreateForm
from tenders.models import Request, Tender
from tenders.utils.sending_emails import sending_emails_start_tender


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
            sending_emails_start_tender(request=request, tender=tender)

        elif "cancel" in request.POST:
            tender.status = Tender.StatusChoices.CANCELED
            tender.save()

        elif "select_winner" in request.POST:
            tender.status = Tender.StatusChoices.EXECUTED
            tender.save()
            tender_request = Request.objects.get(pk=request.POST.get("tender_request_pk"))
            tender_request.winner = True
            tender_request.save()

        _success_url = reverse_lazy("tenders:buyer_tender_details", kwargs={"pk": tender.pk})
        return HttpResponseRedirect(_success_url)


class BuyerTendersView(LoginRequiredMixin, BuyerTypeRequiredMixin, FilterView):
    template_name = "tenders/buyer_tenders.html"
    filterset_class = TendersBuyerFilter


class SellerTendersView(LoginRequiredMixin, SellerTypeRequiredMixin, FilterView):
    template_name = "tenders/seller_tenders.html"
    filterset_class = TendersSellerFilter


class TendersView(FilterView):
    template_name = "tenders/tenders.html"
    filterset_class = TendersFilter


class TenderDetailsView(TemplateView):
    template_name = "tenders/tender_details.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        tender = get_object_or_404(Tender, pk=kwargs.get("pk"))

        if tender.status == Tender.StatusChoices.NEW:
            return HttpResponseRedirect(reverse_lazy("tenders:all_tender"))

        tender_request = None
        if request.user.is_authenticated:
            if request.user.user_type == get_user_model().TypeChoices.SELLER:
                tender_request = Request.objects.filter(tender=tender).filter(seller=request.user.seller_profile)

        if isinstance(tender_request, QuerySet) and tender_request:
            tender_request = tender_request[0]

        context["tender"] = tender
        context["tender_request"] = tender_request

        return self.render_to_response(context)


class SellerCreateTenderRequestPostView(LoginRequiredMixin, SellerTypeRequiredMixin, View):
    http_method_names = [
        "post",
    ]

    def post(self, request, *args, **kwargs):
        tender = get_object_or_404(Tender, pk=request.POST.get("tender"))
        seller = request.user.seller_profile

        tender_request = Request(
            tender=tender,
            seller=seller,
            total_price=request.POST.get("total_price"),
        )
        tender_request.save()

        return HttpResponseRedirect(reverse_lazy("tenders:tender_details", kwargs={"pk": tender.pk}))


class SellerDeleteTenderRequestPostView(SellerCreateTenderRequestPostView):
    def post(self, request, *args, **kwargs):
        print(request.POST.get("tender_request_pk"))
        tender_request = get_object_or_404(Request, pk=request.POST.get("tender_request_pk"))
        tender_request.delete()

        return HttpResponseRedirect(
            reverse_lazy("tenders:tender_details", kwargs={"pk": request.POST.get("tender_pk")})
        )
