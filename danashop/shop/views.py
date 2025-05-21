from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from authentication.models import CustomUser
from .models import *
from .serializers import *
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
from rest_framework import serializers

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at']

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())

@method_decorator(name='get', decorator=product_filter)
class ProductFilterView(APIView):
    def get(self, request):
        category_id = request.query_params.get('category', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        search = request.query_params.get('search', None)
        in_stock = request.query_params.get('in_stock', None)

        products = Product.objects.all()
        if category_id:
            try:
                category_id = int(category_id)
                category = Category.objects.get(id=category_id)
                subcategories = category.subcategories.all()
                subcategory_ids = [subcategory.id for subcategory in subcategories]
                subcategory_ids.append(category_id)
                products = products.filter(category_id__in=subcategory_ids)
            except (ValueError, Category.DoesNotExist):
                pass 

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        if search:
            products = products.filter(name__iregex=search)

        if in_stock is not None:
            products = products.filter(in_stock=(in_stock.lower() == 'true'))

        serializer = ProductFilterSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateDefaults(APIView):
    def get(self, request):
        try:
            electronics = Category.objects.create(name="Electronics", description="Electronic devices")
     
            phones = Category.objects.create(name="Phones", description="Smartphones and mobile phones", parent=electronics)
            laptops = Category.objects.create(name="Laptops", description="Laptops and notebooks", parent=electronics)
     
            smartphones = Category.objects.create(name="Smartphones", description="High-end smartphones", parent=phones)

        except Exception as e:
            print(f"Error creating categories: {e}")
        return   Response({"message": "Default categories created successfully"}, status=status.HTTP_201_CREATED)
    
class CategoryList(APIView):
    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True) 
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductDetail(APIView):
    serializer_class = ProductSerializer
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
@method_decorator(name='get', decorator=cart_get)
@method_decorator(name='post', decorator=cart_post)
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += int(quantity) 
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()
        return Response({"message": "Product added to cart successfully."}, status=status.HTTP_201_CREATED)
    
@method_decorator(name='put', decorator=cart_update)
class CartModifyView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = cart.items.get(product_id=pk)
            cart_item.delete()
            return Response({"message": "Product removed from cart successfully."}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = cart.items.get(product_id=pk)
            cart_item.quantity = request.data.get('new_quantity', cart_item.quantity)
            cart_item.save()
            return Response({"message": "Cart was updated successfully."}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Product not found in cart"}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(name='post', decorator=order_post)
class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            cart = Cart.objects.get(id=request.data.get('cart_id'))
        except Cart.DoesNotExist:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
            
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            shipping_address=request.data.get('shipping_address'),
            phone_number=request.data.get('phone_number'),
            cart=cart,
            order_date=timezone.now()
        )
        cart.items.all().delete() 
        return Response({"message": "Order placed successfully."}, status=status.HTTP_201_CREATED)