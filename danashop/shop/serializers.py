from rest_framework import serializers
from .models import  Category, Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        error_messages={
            "does_not_exist": "Invalid category. Please select a valid one.",
            "incorrect_type": "Category ID must be an integer.",
        }
    )
    class Meta:
        model = Product
        fields = '__all__'  # Include all fields from the Product model
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Product name cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Product name must be at least 3 characters long.")
        if len(value) > 100:
            raise serializers.ValidationError("Product name cannot exceed 100 characters.")
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError("Product with this name already exists.")
        return value

    def create(self, validated_data):
        user = Product.objects.create(**validated_data)
        return user
