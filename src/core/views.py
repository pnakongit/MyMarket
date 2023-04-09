from django.shortcuts import render  # NOQA : F401
from django.views.generic import TemplateView

from accounts.models import SellerProfile
from shops.models import Brand, Category, Product


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):
        _product_limit_on_page = 8
        _seller_limit_on_page = 4
        context = self.get_context_data(**kwargs)

        category = Category.objects.all()
        brands = Brand.objects.all()
        products = Product.objects.filter(pk__lte=_product_limit_on_page)
        sellers = SellerProfile.objects.filter(rang__gte=SellerProfile.objects.count() - _seller_limit_on_page)

        context.update({"category": category, "brands": brands, "products": products, "sellers": sellers})

        return self.render_to_response(context)
