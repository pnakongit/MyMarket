from django.db.models import Q

from shops.models import Product


def add_shopping_cart_information_to_session(request, product_pk, quantity=None, delete=False):
    if not request.session.get("shopping_cart"):
        request.session["shopping_cart"] = {}

    if delete:
        request.session["shopping_cart"].pop(f"{product_pk}", None)
    else:
        request.session["shopping_cart"].update({product_pk: quantity})

    request.session.save()


def get_shopping_cart_data(request):
    shopping_cart = request.session.get("shopping_cart", None)

    or_filter = Q()
    for product in shopping_cart:
        or_filter |= Q(pk=product)

    products = Product.objects.filter(or_filter)

    shopping_cart_data = {}
    total_price = 0

    for product in products:
        total_price_of_product = product.price * shopping_cart.get(f"{product.pk}")
        shopping_cart_data.update(
            {
                product.pk: {
                    "product_name": product.product_name,
                    "product_price": product.price,
                    "count": shopping_cart.get(f"{product.pk}"),
                    "total_price_of_product": total_price_of_product,
                    "seller": product.seller.brand_name,
                    "url": product.image.url if product.image else "",
                }
            }
        )
        total_price += total_price_of_product

    return {"shopping_cart_data": shopping_cart_data, "total_price": total_price}
