from django.forms import ModelForm

from tenders.models import ProductParameter, Tender


class TenderCreateForm(ModelForm):
    class Meta:
        model = Tender
        fields = ["tender_name", "description", "end_day", "minimum_required_rank"]


class CreateProductParameterForm(ModelForm):
    class Meta:
        model = ProductParameter
        fields = ["products", "amount", "category", "brand"]
