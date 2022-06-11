from django.http import JsonResponse
from django.templatetags.static import static
from phonenumbers import is_valid_number_for_region, parse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .models import Order, OrderItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def get_order_error_content(received_order):
    order_keys = [
        'products',
        'firstname',
        'lastname',
        'phonenumber',
        'address',
    ]
    for order_key in order_keys:
        if not order_key in received_order:
            return {order_key: 'Обязательное поле.'}
        if received_order[order_key] is None:
            return {order_key: 'Это поле не может быть пустым.'}
        if received_order[order_key] == '':
            return {order_key: 'Это поле не может быть пустым.'}
    
    if isinstance(received_order['products'], str):
        return {'products': 'Ожидался list со значениями, но был получен str.'}
    
    string_order_keys = ['firstname', 'lastname', 'phonenumber', 'address']
    for order_key in string_order_keys:
        if not isinstance(received_order[order_key], str):
            return {order_key: 'Not a valid string.'}

    if received_order['products'] == []:
        return {'products': 'Этот список не может быть пустым.'}
    
    if not is_valid_number_for_region(parse(received_order['phonenumber'], 'RU'), 'RU'):
        return {'phonenumber': 'Введен некорректный номер телефона.'}

    for position in received_order['products']:
        if not Product.objects.filter(id=position['product']):
            return {'product': 'Недопустимый первичный ключ "{}"'.format(position['product'])}


@api_view(['POST'])
def register_order(request):
    received_order = request.data
    print(received_order)
    order_error_content = get_order_error_content(received_order)
    if order_error_content:
        return Response(order_error_content, status=status.HTTP_406_NOT_ACCEPTABLE)
    order = Order.objects.create(
        firstname=received_order['firstname'],
        lastname=received_order['lastname'],
        phonenumber=received_order['phonenumber'],
        address=received_order['address'],
    )
    for position in received_order['products']:
        product = Product.objects.get(id=position['product'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=position['quantity'],
        )
    
    return Response()
