from rest_framework import serializers

from foodcartapp.models import OrderProduct, Order, Product


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, allow_empty=False, write_only=True)

    def create(self, validated_data):
        order = Order.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            address=validated_data['address'],
            phonenumber=validated_data['phonenumber']
        )
        products = validated_data['products']
        for product in products:
            order.products.add(product['product'], through_defaults={
                'quantity': product.get('quantity'),
                'price': product['product'].price
            })

        return order

    class Meta:
        model = Order
        fields = ['id', 'products', 'firstname', 'lastname', 'address', 'phonenumber']
