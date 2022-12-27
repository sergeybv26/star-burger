import json
from pprint import pprint

from django.http import JsonResponse
from django.templatetags.static import static


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


def register_order(request):
    try:
        new_order = json.loads(request.body.decode())
    except ValueError:
        return JsonResponse({
            'error': 'В запросе необходимо передать JSON',
        })
    try:
        order = Order.objects.create(
            firstname=new_order.get('firstname', ''),
            lastname=new_order.get('lastname', ''),
            address=new_order.get('address'),
            phonenumber=new_order.get('phonenumber')
        )
        for product in new_order.get('products'):
            order.products.add(product.get('product'), through_defaults={'quantity': product.get('quantity')})
    except Exception as err:
        return JsonResponse(
            {'error': err}
        )

    return JsonResponse({})
