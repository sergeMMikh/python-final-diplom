import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from rest_framework import status
from rest_framework.authtoken.models import Token
from orders.models import User, Shop, Category, Product, ProductInfo
from faker import Faker
from .test_utils import base_url, base_url_user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_4_shop_factory(client):
    def factory(*args, **kwargs):
        user = baker.make(User, *args, **kwargs)
        token = Token.objects.create(user=user)
        return user, token

    return factory

@pytest.fixture()
def shop_factory():
    def factory(*args, **kwargs):
        return baker.make(Shop, *args, **kwargs)
    return factory

@pytest.fixture()
def category_factory():
    def factory(*args, **kwargs):
        return baker.make(Category, *args, **kwargs)
    return factory

@pytest.fixture()
def product_factory(shop_factory):
    def factory(*args, **kwargs):
        faker = Faker()
        shop = shop_factory()
        product = Product.objects.create(
            name=faker.name(),
            category=baker.make(Category,
                                *args, **kwargs)
        )
        baker.make(ProductInfo,
                   shop=shop,
                   product=product,
                   *args, **kwargs)
        return product
    return factory


@pytest.fixture
def shop_user_factory(client, user_4_shop_factory):
    def factory(*args, **kwargs):
        user, token = user_4_shop_factory()

        response = client.get(path=f'{base_url_user}verify_email/{token}/')

        headers = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        response = client.post(f'{base_url_user}details',
                               data={
                                   'user_type': 'shop',
                               },
                               follow=True,
                               **headers)
        user_id = response.data.get('id')
        user = User.objects.get(pk=user_id)

        return user, token

    return factory


@pytest.mark.django_db
def test_shops_list(client, shop_factory):
    response = client.get(path=f'{base_url}shops')

    assert response.status_code == status.HTTP_200_OK

    shops_count = response.data.get('count')

    shop_factory()

    response = client.get(path=f'{base_url}shops')

    assert response.data.get('count') == shops_count + 1

@pytest.mark.django_db
def test_basket(client,
                shop_user_factory,
                product_factory):
    user, token = shop_user_factory()

    product = product_factory()

    headers = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    # test add products to basket
    message = f'[{{"id": {product.id},"quantity": 5}}]'
    response = client.post(f'{base_url}basket',
                           data={
                               'items': message,
                           },
                           follow=True,
                           **headers)
    assert response.status_code == status.HTTP_201_CREATED
