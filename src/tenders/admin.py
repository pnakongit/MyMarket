from django.contrib import admin

from tenders.models import ProductParameter, Request, Tender

admin.site.register(Tender)
admin.site.register(ProductParameter)
admin.site.register(Request)
