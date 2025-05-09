
from django.urls import path

from . import views
from .views import CategoryList, CreateDefaults, EditReviewView, PostReviewView, ProductList, ProductCreate,ProductFilterView, ProductDetail, ProductUpdate, ProductDelete, ReviewListView

urlpatterns = [
  path('products/list/', ProductList.as_view(), name='product-list'),
  path('products/create/', ProductCreate.as_view(), name='product-create'),
  path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
  path('products/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
  path('products/<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
  path('products/filter/', ProductFilterView.as_view(), name='product-filter'),
  path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='product-reviews'),
  path('products/<int:product_id>/post_review/', PostReviewView.as_view(), name='post-review'),
  path('products/<int:product_id>/edit_review/', EditReviewView.as_view(), name='edit-review'),
  path('createdefaults/', CreateDefaults.as_view(), name='create-defaults'),
  path('categories/', CategoryList.as_view(), name='category-list'),

]
