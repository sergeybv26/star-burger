from django import template

register = template.Library()


@register.filter('get_order_param')
def get_order_param(orders_param, order_id):
    if order_id:
        return orders_param.get(order_id)
