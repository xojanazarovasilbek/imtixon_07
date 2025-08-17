from rest_framework import serializers
from .models import Card, CardItem


class CardItemsSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CardItem
        fields = ['id', 'product', 'amount', 'created_at', 'updated_at', 'total_price']


class CardSerializer(serializers.ModelSerializer):
    items = CardItemsSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Card
        fields = ['id', 'user', 'created_at', 'total_price', 'items']
