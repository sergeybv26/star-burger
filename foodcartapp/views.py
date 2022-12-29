import json
from pprint import pprint

from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from phonenumber_field.validators import validate_international_phonenumber

from .models import Product, Order


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


@api_view(['POST'])
def register_order(request):
    # orders = Order.objects.all()
    new_order = request.data
    if not new_order:
        return Response(
            {'error': 'В запросе необходимо передать JSON'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    products = new_order.get('products')
    if not products or not isinstance(products, list):
        return Response(
            {'error': 'Поле products отсутствует или не является списком'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    firstname = new_order.get('firstname')
    if not firstname or not isinstance(firstname, str):
        return Response(
            {'error': 'Поле firstname отсутствует или не является строкой'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    lastname = new_order.get('lastname')
    if not lastname or not isinstance(lastname, str):
        return Response(
            {'error': 'Поле lastname отсутствует или не является строкой'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    address = new_order.get('address')
    if not address or not isinstance(address, str):
        return Response(
            {'error': 'Поле address отсутствует или не является строкой'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    phonenumber = new_order.get('phonenumber')
    if not phonenumber:
        return Response(
            {'error': 'Поле phonenumber не может быть пустым'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    try:
        validate_international_phonenumber(phonenumber)
    except ValidationError as err:
        return Response(
            {'error': err},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
    try:
        order = Order.objects.create(
            firstname=firstname,
            lastname=lastname,
            address=address,
            phonenumber=phonenumber
        )
        for product in products:
            product_obj = Product.objects.get(pk=product.get('product'))
            order.products.add(product_obj, through_defaults={'quantity': product.get('quantity')})
    except Product.DoesNotExist:
        return Response(
            {'error': 'Не верный ID продукта'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )

    return Response({})
