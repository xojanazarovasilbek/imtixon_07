from rest_framework import serializers
from order.models import OrderItem, Order


class OrderItemsSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'amount', 'created_at', 'updated_at', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True, read_only=True)  
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'items']