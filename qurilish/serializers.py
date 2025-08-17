from rest_framework import serializers
from .models import Product, Comments


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Comments
        fields = ['id', 'user', 'post', 'text', 'created_at', 'updated_at']