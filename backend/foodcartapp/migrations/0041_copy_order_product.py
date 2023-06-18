# Generated by Django 3.2.15 on 2023-01-02 16:53

from django.db import migrations
from itertools import chain


def copy_product_in_order(apps, schema_editor):
    OrderProduct = apps.get_model('foodcartapp', 'OrderProduct')
    OrderProductNew = apps.get_model('foodcartapp', 'OrderProductNew')

    order_product_set = OrderProduct.objects.all().select_related('product')
    if order_product_set:
        order_product_iterator = order_product_set.iterator()
        for order_product in chain(order_product_iterator):
            OrderProductNew.objects.get_or_create(
                order=order_product.order,
                product=order_product.product,
                quantity=order_product.quantity,
                price=order_product.product.price
            )


class Migration(migrations.Migration):
    dependencies = [
        ('foodcartapp', '0040_orderproductnew'),
    ]

    operations = [
        migrations.RunPython(copy_product_in_order)
    ]