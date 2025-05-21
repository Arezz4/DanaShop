from rest_framework import serializers
from danashop.models import *
from drf_extra_fields.fields import Base64ImageField 

class ProductFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'in_stock', 'created_at', 'image', 'specifications']

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    price_per_item = serializers.SerializerMethodField() 
    total_price = serializers.SerializerMethodField() 

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'price_per_item', 'total_price']

    def get_price_per_item(self, obj):
        return obj.product.price

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity
    
class ProductSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False) 
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        error_messages={
            "does_not_exist": "Invalid category. Please select a valid one.",
            "incorrect_type": "Category ID must be an integer.",
        }
    )
    average_rating = serializers.SerializerMethodField()  

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'in_stock', 'created_at', 'image', 'specifications', 'average_rating']

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

    def get_average_rating(self, obj):
        return obj.average_rating()
    
    def validate_image(self, value):
        max_size_mb = 5
        max_size_bytes = max_size_mb * 1024 * 1024  
        if value.size > max_size_bytes:
            raise serializers.ValidationError(f"Image size cannot exceed {max_size_mb} MB.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return CategorySerializer(subcategories, many=True).data
    
