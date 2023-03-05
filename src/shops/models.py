from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField


class Product(models.Model):
    product_name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='accounts/uploads/', null=True, blank=True)
    description = models.CharField(max_length=300)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='UAH')
    available = models.BooleanField(default=True)
    seller = models.ForeignKey(to="accounts.SellerProfile", related_name="product", on_delete=models.CASCADE)
    category = models.ForeignKey(to="shops.Category", related_name="product", on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(to="shops.Brand", related_name="product", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product_name


class Category(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='accounts/uploads/', null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='accounts/uploads/', null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class StatusChoices(models.IntegerChoices):
        NEW = 0, "New"
        EXECUTED = 1, "Executed"

    buyer = models.ForeignKey(to="accounts.BuyerProfile", related_name="order", on_delete=models.CASCADE)
    product = models.ForeignKey(to="shops.Product", related_name='order', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.PositiveIntegerField(choices=StatusChoices.choices, default=StatusChoices.NEW)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='UAH', default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.amount * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.buyer} - {self.product}"
