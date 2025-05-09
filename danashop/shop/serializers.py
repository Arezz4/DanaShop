from rest_framework import serializers
from .models import  Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description']
    def create(self, validated_data):
        user = Product.objects.create(**validated_data)
        return user
