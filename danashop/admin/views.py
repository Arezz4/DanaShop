from danashop.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from danashop.models import  *
from danashop.serializers import  *
from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from django.utils.decorators import method_decorator
from .docs.swagger_docs import *

from rest_framework import status
from danashop.models import Product

@method_decorator(name='put', decorator=product_update)
class ProductModifyView(APIView):
    permission_classes = [IsAdminUser] 
    serializer_class = ProductSerializer

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Product has been updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return Response({"message": "Product has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
@method_decorator(name='post', decorator=product_create)
class ProductView(APIView):
    permission_classes = [IsAdminUser] 
    serializer_class = ProductSerializer
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product has been created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(name='post', decorator=category_create)
class CategoryView(APIView):
    # permission_classes = [IsAdminUser] 
    
    def get(self, request):
        categories = Category.objects.filter(parent__isnull=True) 
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category has been created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(name='put', decorator=category_update)
class CategoryModifyView(APIView):
    # permission_classes = [IsAdminUser] 
    serializer_class = CategorySerializer

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Category has been updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({"message": "Category has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@method_decorator(name='put', decorator=order_update)
class OrderModifyView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.status = request.data.get('status')
            order.save()
            return Response({"message": "Order has been updated successfully."}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
