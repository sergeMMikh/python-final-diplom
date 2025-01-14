from rest_framework import status

from orders.models import Order, OrderItem, ProductInfo
from django.db.models import Q, F, Sum
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework.views import APIView
from ujson import loads as load_json

from pprint import pprint
from orders.serializers import OrderSerializer, OrderAddItemSerializer

"""
Порядок действий пользователя для заказа

    Вход/регистрация
    Выбор фильтров в каталоге товаров
        Выбор магазинов (по необходимости)
        Выбор категории (по необходимости)
    Выбор товара
    Выбор количества, цены/магазина
    Экран "Корзина"
    Экран "Подтверждение заказа"
    Экран "Спасибо за заказ"

    После подтверждения заказа, нужно отправить 
    email пользователю (покупателю) и администратору (для исполнения заказа)
"""


class BasketView(APIView):
    """
    Класс для работы с корзиной пользователя
    """

    # получить корзину
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        basket = Order.objects.filter(
            user_id=request.user.id, state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').annotate(
            total_sum=Sum(
                F('ordered_items__quantity')
                * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    # редактировать корзину
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=status.HTTP_403_FORBIDDEN)

        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = load_json(items_sting)
                print("items_dict")
                pprint(items_dict)
            except ValueError:
                JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'},
                             status=status.HTTP_400_BAD_REQUEST)
            else:
                basket, _ = Order.objects.get_or_create(
                    user_id=request.user.id,
                    state='basket')
                print('basket:')
                pprint(basket)
                objects_created = 0
                for order_item in items_dict:
                    order_item.update({
                        'order': basket.id})
                    product = ProductInfo.objects.get(product_id=order_item.get('id'))
                    new_order_item = {
                        'order': basket.id,
                        'product_info': product.id,
                        'quantity': order_item.get('quantity'),
                        'shop': product.shop.id,
                    }
                    print('new_order_item:')
                    pprint(new_order_item)
                    serializer = OrderAddItemSerializer(data=new_order_item)
                    print('serializer')
                    if serializer.is_valid():
                        try:
                            serializer.save()
                        except IntegrityError:
                            return JsonResponse({'Status': False,
                                                 'Errors': 'Order alredy exists'},
                                                status=status.HTTP_400_BAD_REQUEST)
                        except Exception as error:
                            print(f"Error: {str(error)}")
                            return JsonResponse({'Status': False,
                                                 'Errors': str(error)},
                                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            objects_created += 1

                    else:
                        JsonResponse({'Status': False,
                                      'Errors': serializer.errors})

                return JsonResponse(
                    {'Status': True,
                     'Создано объектов': objects_created},
                    status=status.HTTP_201_CREATED)
        return JsonResponse(
            {'Status': False,
             'Errors': 'Не указаны все необходимые аргументы'},
            status=status.HTTP_400_BAD_REQUEST)

    # удалить товары из корзины
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'},
                                status=status.HTTP_403_FORBIDDEN)

        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            basket, _ = Order.objects.get_or_create(
                user_id=request.user.id,
                state='basket')
            query = Q()
            objects_deleted = False
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    query = query | Q(order_id=basket.id, id=order_item_id)
                    objects_deleted = True

            if objects_deleted:
                deleted_count = OrderItem.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True,
                                     'Удалено объектов': deleted_count})
        return JsonResponse({'Status': False,
                             'Errors': 'Не указаны все необходимые аргументы'},
                            status=status.HTTP_400_BAD_REQUEST)

    # добавить позиции в корзину
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False,
                                 'Error': 'Log in required'},
                                status=status.HTTP_403_FORBIDDEN)

        items_sting = request.data.get('items')

        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                return JsonResponse({'Status': False,
                                     'Errors': 'Неверный формат запроса'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                basket, _ = Order.objects.get_or_create(
                    user_id=request.user.id,
                    state='basket')
                objects_updated = 0
                for order_item in items_dict:
                    print('order_item:')
                    print(order_item)
                    print(f"order_item['id']: {order_item['id']}")
                    print(f"order_item['quantity']: {order_item['quantity']}")
                    if type(order_item['id']) == int \
                            and type(order_item['quantity']) == int:

                        try:
                            obj, created = OrderItem.objects.update_or_create(
                                order_id=basket.id,
                                product_info_id=order_item['id'],
                                shop_id=3,
                                quantity=order_item['quantity'])
                            if created:
                                print("Created!")
                            else:
                                print("Updated!")
                            objects_updated += 1
                        except IntegrityError:
                            return JsonResponse({'Status': False,
                                                 'Errors': 'Неверный запрос'},
                                                status=status.HTTP_400_BAD_REQUEST)
                        except Exception as error:
                            return JsonResponse({'Status': False, 'Errors': str(error)})
                    else:
                        return JsonResponse({'Status': False,
                                             'Errors': 'Неверный формат запроса'},
                                            status=status.HTTP_400_BAD_REQUEST)

                return JsonResponse(
                    {'Status': True,
                     'Обновлено объектов': objects_updated},
                    status=status.HTTP_202_ACCEPTED)

        return JsonResponse(
            {'Status': False,
             'Errors': 'Не указаны все необходимые аргументы (items_sting)'},
            status=status.HTTP_400_BAD_REQUEST)
