from datetime import date, timedelta

from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField

from shops.models import Product


class Tender(models.Model):
    TENDER_EXPIRATION_DAYS = 10

    class StatusChoices(models.IntegerChoices):
        NEW = 0, "New"
        PUBLISHED = 1, "Published"
        EXECUTED = 2, "Executed"
        CANCELED = 3, "Canceled"

    tender_name = models.CharField(max_length=200, default="")
    buyer = models.ForeignKey(
        to="accounts.BuyerProfile", related_name="tender", on_delete=models.CASCADE, blank=True, null=True
    )
    end_day = models.DateField(default=date.today() + timedelta(days=TENDER_EXPIRATION_DAYS))
    description = models.TextField(max_length=500, default="")
    status = models.PositiveIntegerField(choices=StatusChoices.choices, default=StatusChoices.NEW)
    minimum_required_rank = models.PositiveIntegerField(default=0)

    def get_seller_email_for_mailing(self) -> list:
        product_names_lst = [product.products for product in self.product_parameter.all()]

        products = Product.objects.filter(product_name__in=product_names_lst)
        emails_list = []
        for product in products:
            emails_list.append(product.seller.customer.email)

        return emails_list

    def __str__(self):
        return f"{self.buyer} tender {self.pk}"


class ProductParameter(models.Model):
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    products = models.CharField(max_length=150)
    category = models.ForeignKey(to="shops.Category", related_name="product_parameter", on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(to="shops.Brand", related_name="product_parameter", on_delete=models.SET_NULL, null=True)
    tender = models.ForeignKey(
        to="tenders.Tender", related_name="product_parameter", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.tender} - {self.products}"


class Request(models.Model):
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='UAH')
    seller = models.ForeignKey(to="accounts.SellerProfile", related_name="request", on_delete=models.CASCADE)
    tender = models.ForeignKey(
        to="tenders.Tender", related_name="request", on_delete=models.CASCADE, blank=True, null=True
    )
    winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seller} request {self.pk}"
