
from django.urls import path
from . import views

urlpatterns = [
  path('shop/product-list/', views.ProductList.as_view(), name='product-list')
]
