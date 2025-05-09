
from django.urls import path

from . import views
from .views import ProductList, ProductCreate, ProductDetail, ProductUpdate, ProductDelete

urlpatterns = [
  path('products/list/', ProductList.as_view(), name='product-list'),
  path('products/create/', ProductCreate.as_view(), name='product-create'),
  path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
  path('products/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
  path('products/<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),

]
