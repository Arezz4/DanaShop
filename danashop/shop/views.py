from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from authentication.models import CustomUser
from .models import Category, Product
from .serializers import CategorySerializer, ProductFilterSerializer, ProductSerializer, ReviewSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from .docs.swagger_docs import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer
@method_decorator(name='get', decorator=product_filter)
class ProductFilterView(APIView):
    def get(self, request):
        # Get query parameters
        category_id = request.query_params.get('category', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        search = request.query_params.get('search', None)
        in_stock = request.query_params.get('in_stock', None)

        # Start with all products
        products = Product.objects.all()
        # Filter by category (ensure category_id is an integer)
        if category_id:
            try:
                category_id = int(category_id)
                # Get the selected category
                category = Category.objects.get(id=category_id)
                # Get all subcategories recursively
                subcategories = category.subcategories.all()
                subcategory_ids = [subcategory.id for subcategory in subcategories]
                subcategory_ids.append(category_id)  # Include the parent category
                products = products.filter(category_id__in=subcategory_ids)
            except (ValueError, Category.DoesNotExist):
                pass  # Ignore invalid category_id values or non-existent categories

        # Filter by price range
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        # Filter by search regex in name
        if search:
            products = products.filter(name__iregex=search)

        # Filter by stock availability
        if in_stock is not None:
            products = products.filter(in_stock=(in_stock.lower() == 'true'))

        # Serialize the filtered products
        serializer = ProductFilterSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
@method_decorator(name='post', decorator=product_review)
class PostReviewView(APIView):
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required to post a review."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            product = Product.objects.get(id=product_id)
            # Check if the user has already posted a review for this product
            if product.reviews.filter(user=request.user).exists():
                return Response({"error": "You have already posted a review for this product."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(product=product, user=request.user)  # Save with the authenticated user
                return Response({"message": "Your review has been posted successfully."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
class ReviewListView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            reviews = product.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
@method_decorator(name='post', decorator=product_review)
class EditReviewView(APIView):
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required to edit a review."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            product = Product.objects.get(id=product_id)
            # Check if the user has a review for this product
            review = product.reviews.filter(user=request.user).first()
            if not review:
                return Response({"error": "You have not posted a review for this product."}, status=status.HTTP_404_NOT_FOUND)

            serializer = ReviewSerializer(review, data=request.data, partial=True)  # Allow partial updates
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Your review has been updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
class CreateDefaults(APIView):
    def get(self, request):
        try:
            
              # Create a top-level category
              electronics = Category.objects.create(name="Electronics", description="Electronic devices")
     
              # Create subcategories
              phones = Category.objects.create(name="Phones", description="Smartphones and mobile phones", parent=electronics)
              laptops = Category.objects.create(name="Laptops", description="Laptops and notebooks", parent=electronics)
     
              # Create a subcategory of a subcategory
              smartphones = Category.objects.create(name="Smartphones", description="High-end smartphones", parent=phones)

        except Exception as e:
            print(f"Error creating categories: {e}")
        return   Response({"message": "Default categories created successfully"}, status=status.HTTP_201_CREATED)
class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True)  # Get only top-level categories
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
@method_decorator(name='post', decorator=product_create)
class ProductCreate(APIView):
    serializer_class = ProductSerializer

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product has been created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetail(APIView):
    serializer_class = ProductSerializer
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(name='post', decorator=product_update)
class ProductUpdate(APIView):
    serializer_class = ProductSerializer

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product has been updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class ProductDelete(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can access this view

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({"message": "Product has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)