from datetime import date, timedelta

from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField


class Tender(models.Model):
    TENDER_EXPIRATION_DAYS = 10

    class StatusChoices(models.IntegerChoices):
        NEW = 0, "New"
        EXECUTED = 1, "Executed"

    buyer = models.ForeignKey(to="accounts.BuyerProfile", related_name="tender", on_delete=models.CASCADE)
    end_day = models.DateField(default=date.today() + timedelta(days=TENDER_EXPIRATION_DAYS))
    description = models.CharField(max_length=300, null=True, blank=True)
    status = models.PositiveIntegerField(choices=StatusChoices.choices, default=StatusChoices.NEW)

    def __str__(self):
        return f"{self.buyer} tender {self.pk}"


class ProductParameter(models.Model):
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    products = models.ForeignKey(to="shops.Product", related_name="product_parameter", on_delete=models.CASCADE)
    tender = models.ForeignKey(to="tenders.Tender", related_name="product_parameter", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tender} - {self.products}"


class Request(models.Model):
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='UAH')
    seller = models.ForeignKey(to="accounts.SellerProfile", related_name="Request", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.seller} request {self.pk}"
