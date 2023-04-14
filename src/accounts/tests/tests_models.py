from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.test import TestCase
from faker import Faker

from accounts.models import Customer


class TestCustomerModel(TestCase):
    faker = Faker('UK')

    def test_get_all_buyers(self):
        _count_user = 5
        for i in range(_count_user):
            Customer.objects.create(
                email=self.faker.email(), phone_number=f"+38063991800{i}", password=make_password('testpass')
            )
        self.assertEqual(Customer.get_all_buyers().count(), _count_user)

    def test_get_all_seller(self):
        _count_user = 10

        for i in range(_count_user):
            Customer.objects.create(
                email=self.faker.email(),
                phone_number=f"+38063991800{i}",
                password='testpass',
                user_type=1,
            )
        self.assertEqual(Customer.get_all_seller().count(), _count_user)

    def test_phonenumber_validation(self):
        with self.assertRaises(ValidationError):
            Customer.objects.create(
                email=self.faker.email(),
                phone_number="063-991-81-11",
                password='testpass',
                user_type=1,
            )

    def test_email_validation(self):
        with self.assertRaises(ValidationError):
            Customer.objects.create(
                email='admin123@admim',
                phone_number="+38-063-991-81-11",
                password='testpass',
            )
