from django.contrib import admin

from accounts.models import BuyerProfile, Customer, SellerProfile

# Register your models here.
admin.site.register(Customer)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
