from django.contrib import admin

from shops.models import Brand, Category, Order, Product

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Order)
