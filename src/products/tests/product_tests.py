from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker

from products.models import Product


class TestProduct(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.product = baker.make(Product, title='Bat')

    def test_product(self):
        self.product.price = 10000
        self.product.save()
        print(self.product.slug)
        assert self.product.slug is None

