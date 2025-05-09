
from django.urls import path

from . import views
from .views import CartView, CategoryList, CreateDefaults, DiscountCodeCreateView, DiscountCodeDeleteView, DiscountCodeView, EditReviewView,ShippingAddressCreateView, PostReviewView, ProductList, ProductCreate,ProductFilterView, ProductDetail, ProductUpdate, ProductDelete, ReviewListView, ShippingAddressDeleteView, ShippingAddressListView, ShippingAddressUpdateView

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
  path('cart/', CartView.as_view(), name='cart'),
  path('shipping-addresses/list', ShippingAddressListView.as_view(), name='shipping-address-list'),
  path('shipping-addresses/create', ShippingAddressCreateView.as_view(), name='shipping-address-create'),
  path('shipping-addresses/<int:pk>/update', ShippingAddressUpdateView.as_view(), name='shipping-address-update'),
  path('shipping-addresses/<int:pk>/delete', ShippingAddressDeleteView.as_view(), name='shipping-address-delete'),
  path('discount-code/check/', DiscountCodeView.as_view(), name='discount-code'),
  path('discount-code/create/', DiscountCodeCreateView.as_view(), name='discount-code-create'),
  path('discount-code/<int:pk>/delete/', DiscountCodeDeleteView.as_view(), name='discount-code-delete'),

]
