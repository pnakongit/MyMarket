from django.db.models import Q
from faker import Faker

from accounts.models import BuyerProfile, Customer, SellerProfile
from shops.models import Brand, Category, Order, Product


def account_generator(user_type=0):
    faker = Faker()
    customer = Customer(
        email=faker.email(),
        phone_number=f"+38063{faker.random_int(min=100, max=999)}{faker.random_int(min=1000, max=9999)}",
        user_type=user_type
    )
    customer.set_password("12345678")
    customer.save()

    if customer.user_type == 0:
        buyer = BuyerProfile.objects.get(pk=customer.buyer_profile.pk)
        buyer.first_name = faker.first_name()
        buyer.last_name = faker.last_name()
        buyer.save()

    else:
        seller = SellerProfile.objects.get(pk=customer.seller_profile.pk)
        seller.brand_name = faker.company()
        seller.city = faker.city
        seller.save()

    return customer


def product_generator():
    faker = Faker()
    seller = Customer.objects.filter(Q(email__icontains="@example") | Q(user_type=1)).first()
    if not seller:
        seller = account_generator(user_type=1)

    category = Category.objects.all().first()
    if not category:
        category = Category.objects.create(name="test_category")

    brand = Brand.objects.all().first()
    if not brand:
        brand = Brand.objects.create(name="test_barnd")

    product = Product(
        product_name=f"Test product name _ {faker.random_int(max=9999)}",
        description=faker.paragraph(nb_sentences=2),
        price=faker.random_int(min=150, max=15_000),
        seller=SellerProfile.objects.get(pk=seller.seller_profile.pk),
        category=category,
        brand=brand,
    )
    product.save()

    return product


def order_generator():
    faker = Faker()
    buyer = Customer.objects.filter(Q(email__icontains="@example") | Q(user_type=0)).first()
    if not buyer:
        buyer = account_generator(user_type=0)

    product = Product.objects.all().first()
    if not product:
        product = product_generator()

    order = Order(
        buyer=BuyerProfile.objects.get(pk=buyer.buyer_profile.pk),
        product=product,
        amount=faker.random_digit_not_null(),
    )

    order.save()
