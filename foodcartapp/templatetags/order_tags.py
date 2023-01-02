from django import template

register = template.Library()


@register.filter('get_order_cost')
def get_order_cost(orders_cost, order_id):
    if order_id:
        return orders_cost.get(order_id, 0)
