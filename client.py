import requests
from pprint import pprint

url = 'http://127.0.0.1:8000'

# Регистрация

request = requests.post(f'{url}/user/register',
                        data={
                            "first_name": "magaz",
                            "last_name": "magaz5",
                            "email": "magaz5@gmail.com",
                            "password": "adminadmin",
                            "company": "Magaz5",
                            "position": "funcionario",
                            "user_type": "shop",
                        })

data_str = request.json()
print("request:")
pprint(data_str)

# Вход
request = requests.post(f'{url}/user/login',
                        data={
                            "email": "magaz5@gmail.com",
                            "password": "adminadmin",
                        },
                        )
data_str = request.json()
print("request:")
pprint(data_str)

TOKEN = data_str.get('Token')
print(f'TOKEN: {TOKEN}')

# # Обновление списка товаров
# request = requests.post(f'{url}/partner/update',
#                         headers={
#                             'Authorization': f'Token {TOKEN}',
#                         },
#                         data={"url":
#                                   "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1K30Oeujse-05WCEGEFZC6oOX4Q_kACPy"},
#                         )
# print("post:")
# pprint(request.json())
# {"url": "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1K30Oeujse-05WCEGEFZC6oOX4Q_kACPy"}
#
# # Список товаров
# request = requests.get(f'{url}/products/list',
#                        headers={
#                            'Authorization': f'Token {TOKEN}',
#                        },
#                        data={
#                            "page": "1",
#                        },
#                        )
# print("products-list:")
# pprint(request.json())
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
# pprint(request.json())
#
# # Список товаров по категории и магазину
# request = requests.get(f'{url}/products/view',
#                        headers={
#                            'Authorization': f'Token {TOKEN}',
#                        },
#                        data={
#                            "page": "1",
#                            'category': 'Смартфоны',
#                            'shop': 'Связной',
#                        },
#                        )
# print("products-view:")
# pprint(request.json())

# Карточка товара
# request = requests.get(f'{url}/product/view_by_id',
#                        headers={
#                            'Authorization': f'Token {TOKEN}',
#                        },
#                        data={
#                            "product_id": "4",
#                        },
#                        )
# print("products-view:")
# pprint(request.json())


# Карточка товара
# request = requests.get(f'{url}/products/search',
#                        headers={
#                            'Authorization': f'Token {TOKEN}',
#                        },
#                        data={
#                            "product_id": "1",
#                        },
#                        )
# print("products-view:")
# pprint(request.json())

# Корзина


# Добавление товара в корзину
try:
    request = requests.put(f'{url}/basket',
                           headers={
                               'Authorization': f'Token {TOKEN}',
                           },
                           data={
                               'items': '[{"id":1,"quantity":5},{"id":3,"quantity":2}]',
                           },
                           )
except requests.exceptions.JSONDecodeError:
    print("requests.exceptions.JSONDecodeError")

print("request:")
pprint(request.status_code)
if request.status_code == 200:
    pprint(request.json())

# Просмотр корзины
request = requests.get(f'{url}/basket',
                       headers={
                           'Authorization': f'Token {TOKEN}',
                       },
                       data={
                       },
                       )
print("products-view:")
pprint(request.json())
