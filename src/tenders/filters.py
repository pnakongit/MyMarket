from django import forms
from django_filters import CharFilter, DateFilter, FilterSet, NumberFilter

from tenders.models import Tender


class TendersFilter(FilterSet):
    end_date__gt = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), field_name='end_day', lookup_expr=('gt'))
    end_date__lt = DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='end_day',
        lookup_expr=('lt'),
    )
    tender_name = CharFilter(field_name="tender_name", lookup_expr=("icontains"))
    minimum_required_rank = NumberFilter(field_name='minimum_required_rank', lookup_expr='gt')

    class Meta:
        model = Tender
        fields = [
            'minimum_required_rank',
        ]

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(status=Tender.StatusChoices.PUBLISHED)


class TendersBuyerFilter(FilterSet):
    end_date__gt = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), field_name='end_day', lookup_expr=('gt'))
    end_date__lt = DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='end_day',
        lookup_expr=('lt'),
    )
    tender_name = CharFilter(field_name="tender_name", lookup_expr=("icontains"))

    class Meta:
        model = Tender
        fields = [
            "status",
        ]

    @property
    def qs(self):
        parent = super().qs
        buyer_profile = self.request.user.buyer_profile

        return parent.filter(buyer=buyer_profile)


class TendersSellerFilter(FilterSet):
    end_date__gt = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), field_name='end_day', lookup_expr=('gt'))
    end_date__lt = DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        field_name='end_day',
        lookup_expr=('lt'),
    )
    tender_name = CharFilter(field_name="tender_name", lookup_expr=("icontains"))

    class Meta:
        model = Tender
        fields = [
            "status", "tender_name",
        ]

    @property
    def qs(self):
        parent = super().qs
        seller_profile = self.request.user.seller_profile

        return parent.filter(request__seller=seller_profile)
