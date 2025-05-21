
from django.urls import path
from .views import *

urlpatterns = [
  path('products/', ProductList.as_view(), name='product-list'),
  path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
  path('products/filter/', ProductFilterView.as_view(), name='product-filter'),
  path('createdefaults/', CreateDefaults.as_view(), name='create-defaults'),
  path('categories/', CategoryList.as_view(), name='category-list'),
  path('cart/', CartView.as_view(), name='cart'),
  path('cart/<int:pk>/', CartModifyView.as_view(), name='cart-modify-view'),
  path('order/', OrderView.as_view(), name='order'),
]
