
from django.urls import path

from . import views
from .views import *

urlpatterns = [
  path('products/', ProductView.as_view(), name='product-view'),
  path('products/<int:pk>/', ProductModifyView.as_view(), name='product-modify'),
  path('categories/', CategoryView.as_view(), name='category-view'),
  path('categories/<int:pk>/', CategoryModifyView.as_view(), name='category-modify'),
  path('orders/', OrderView.as_view(), name='order-view'),
  path('orders/<int:pk>/', OrderModifyView.as_view(), name='order-modify'),
  
]
