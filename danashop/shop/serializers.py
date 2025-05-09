from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Product

class ProductFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'in_stock', 'created_at', 'image', 'specifications']


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


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        # Recursively serialize subcategories
        subcategories = obj.subcategories.all()
        return CategorySerializer(subcategories, many=True).data