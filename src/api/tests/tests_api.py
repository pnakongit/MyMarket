from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.status import (HTTP_201_CREATED, HTTP_401_UNAUTHORIZED,
                                   HTTP_403_FORBIDDEN)
from rest_framework.test import APIClient

from shops.models import Product


class TestAPI(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.buyer = get_user_model().objects.create(
            email='test@email.com', password="123456", phone_number="+380639918776"
        )

        self.seller = get_user_model().objects.create(
            email='test1@email.com', password="123456", phone_number="+380639918775", user_type=1
        )

    def test_product_detail_no_authenticate(self):
        result = self.client.get(reverse("api:all_products"))
        self.assertEqual(result.status_code, HTTP_401_UNAUTHORIZED)

    def test_product_create_buyer(self):
        self.client.force_authenticate(self.buyer)
        data = {
            "product_name": "test2",
            "description": "test3",
            "price": 4500,
            "seller": 1,
        }
        result = self.client.post(reverse("api:product_create"), data=data)
        self.assertEqual(result.status_code, HTTP_403_FORBIDDEN)

    def test_product_create_seller(self):
        self.client.force_authenticate(self.seller)
        data = {"product_name": "test1", "description": "test2", "price": 1500, "seller": self.seller.seller_profile.pk}
        result = self.client.post(reverse("api:product_create"), data=data)
        self.assertEqual(result.status_code, HTTP_201_CREATED)

    def test_order_create_buyer(self):
        self.client.force_authenticate(self.buyer)

        Product.objects.create(product_name="test1", description="test2", price=1500, seller=self.seller.seller_profile)

        data = {
            "buyer": self.buyer.buyer_profile.pk,
            "product": Product.objects.get(pk=1).pk,
            "amount": 2,
        }

        result = self.client.post(reverse("api:order_create"), data=data)
        self.assertEqual(result.status_code, HTTP_201_CREATED)

    def test_order_create_seller(self):
        self.client.force_authenticate(self.seller)

        Product.objects.create(product_name="test1", description="test2", price=1500, seller=self.seller.seller_profile)
        data = {
            "buyer": 1,
            "product": 1,
            "amount": 2,
        }
        result = self.client.post(reverse("api:order_create"), data=data)
        self.assertEqual(result.status_code, HTTP_403_FORBIDDEN)
