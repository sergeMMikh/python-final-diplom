import requests
from pprint import pprint

url = 'http://127.0.0.1:8000/api/v1/'
TOKEN = None

# Регистрация

request = requests.post(f'{url}user/register',
                        data={
                            "first_name": "magaz",
                            "last_name": "magaz7",
                            "email": "shop_cv@mail.ru",
                            "password": "qwer2345",
                            "company": "Magaz7",
                            "position": "funcionario",
                            "user_type": "shop",
                        })
if request.status_code == 200:
    data_str = request.json()
    print("request:")
    pprint(data_str)
else:
    print(f'request: {request}')

# Вход
request = requests.post(f'{url}user/login',
                        data={
                            "email": "shop_cv@mail.ru",
                            "password": "qwer2345",
                        },
                        )
if request.status_code == 200:
    data_str = request.json()
    print("request:")
    pprint(data_str)

    TOKEN = data_str.get('Token')
    print(f'TOKEN: {TOKEN}')
else:

    print(f'request: {request.status_code}')
    data_str = request.raw
#
# Обновление списка товаров
request = requests.post(f'{url}partner/update',
                        headers={
                            'Authorization': f'Token {TOKEN}',
                        },
                        data={"url":
                                  "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1K30Oeujse-05WCEGEFZC6oOX4Q_kACPy"},
                        )
print("post:")
if request.status_code == 200:
    pprint(request.json())
else:
    print(f'request: {request}')
{"url": "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1K30Oeujse-05WCEGEFZC6oOX4Q_kACPy"}

# # Список товаров
# request = requests.get(f'{url}/api/v1/products/list',
#                        headers={
#                            'Authorization': f'Token {TOKEN}',
#                        },
#                        data={
#                            "page": "1",
#                        },
#                        )
# print("products-list:")
# if request.status_code == 200:
#     pprint(request.json())
# else:
#     print(f'request: {request}')
#
# # Список магазинов
# request = requests.get(f'{url}/shop/list',
#                        headers={
#                            'Authorization': f'Token {TOKEN}',
#                        },
#                        data={
#                            "page": "1",
#                        },
#                        )
# print("shop-list:")
# if request.status_code == 200:
#     pprint(request.json())
#
# # Список товаров по категории и магазину
# print("Список товаров по категории и магазину")
#
# if TOKEN:
#     request = requests.get(f'{url}/products/view',
#                            headers={
#                                'Authorization': f'Token {TOKEN}',
#                            },
#                            data={
#                                "page": "1",
#                                'category': 'Смартфоны',
#                                'shop': 'Связной',
#                            },
#                            )
#     print("products-view:")
#
#     if request.status_code == 200:
#         data_str = request.json()
#         print("request:")
#         pprint(data_str)
#
#         TOKEN = data_str.get('Token')
#         print(f'TOKEN: {TOKEN}')
#     else:
#         print(f'request: {request}')
# else:
#     print('No TOKEN')
#
# # Карточка товара
# request = requests.get(f'{url}/product/view_by_id',
#                        headers={
#                            'Authorization': f'Token {TOKEN}',
#                        },
#                        data={
#                            "product_id": "4",
#                        },
#                        )
# print("products-view:")
# if request.status_code == 200:
#     pprint(request.json())
# else:
#     print(f'request: {request}')
#
# # Карточка товара
# request = requests.get(f'{url}/products/search',
#                        headers={
#                            'Authorization': f'Token {TOKEN}',
#                        },
#                        data={
#                            "product_id": "1",
#                        },
#                        )
# print("products-view:")
# if request.status_code == 200:
#     pprint(request.json())
# else:
#     print(f'request: {request}')
# # Корзина
#
#
# # Добавление товара в корзину
# try:
#     request = requests.put(f'{url}/basket',
#                            headers={
#                                'Authorization': f'Token {TOKEN}',
#                            },
#                            data={
#                                'items': '[{"id":1,"quantity":5},{"id":3,"quantity":2}]',
#                            },
#                            )
# except requests.exceptions.JSONDecodeError:
#     print("requests.exceptions.JSONDecodeError")
#
# print("request:")
# pprint(request.status_code)
# if request.status_code == 200:
#     pprint(request.json())
# else:
#     print(f'request: {request}')
#
# # Просмотр корзины
# request = requests.get(f'{url}/basket',
#                        headers={
#                            'Authorization': f'Token {TOKEN}',
#                        },
#                        data={
#                        },
#                        )
# print("products-view:")
# if request.status_code == 200:
#     pprint(request.json())
# else:
#     print(f'request: {request}')
