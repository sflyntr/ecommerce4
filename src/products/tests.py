import pytest

from products.models import Product


@pytest.mark.django_db
def test_product_list(rf, client):
    obj = Product.objects.create(
        title='hat',
        description='This is hat'
    )
    assert obj


