from rest_framework import serializers
from .models import Cart, CartItem, Category, DiscountCode, Product, Review, ShippingAddress
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Product
from drf_extra_fields.fields import Base64ImageField  # Install this package if not already installed

class ProductFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'in_stock', 'created_at', 'image', 'specifications']
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            'id', 'user', 'full_name', 'phone_number', 'address_line_1', 
            'address_line_2', 'city', 'state', 'postal_code', 'country', 'is_default'
        ]
        read_only_fields = ['user']
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')
    price_per_item = serializers.SerializerMethodField()  # Price per item
    total_price = serializers.SerializerMethodField()  # Total price for the item

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'price_per_item', 'total_price']

    def get_price_per_item(self, obj):
        # Return the price of a single product
        return obj.product.price

    def get_total_price(self, obj):
        # Return the total price for the quantity of the product
        return obj.product.price * obj.quantity
    
class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['id', 'code', 'discount_percentage', 'valid_from', 'valid_until', 'is_active']
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username instead of the user ID

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

    def validate_rating(self, value):
        if value > 5:
            raise serializers.ValidationError("Rating cannot be higher than 5.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)  # Use Base64ImageField for profile pictures
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        error_messages={
            "does_not_exist": "Invalid category. Please select a valid one.",
            "incorrect_type": "Category ID must be an integer.",
        }
    )
    reviews = ReviewSerializer(many=True, read_only=True)  # Include reviews as a nested field
    average_rating = serializers.SerializerMethodField()  # Add average rating as a custom field

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'in_stock', 'created_at', 'image', 'specifications', 'reviews', 'average_rating']

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
        # Use the average_rating method from the Product model
        return obj.average_rating()
    
    def validate_image(self, value):
        # Check the size of the profile picture (max size: 5 MB)
        max_size_mb = 5
        max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
        if value.size > max_size_bytes:
            raise serializers.ValidationError(f"Image size cannot exceed {max_size_mb} MB.")
        return value



class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        # Recursively serialize subcategories
        subcategories = obj.subcategories.all()
        return CategorySerializer(subcategories, many=True).data