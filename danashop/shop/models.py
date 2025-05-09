from django.db import models
from django.db.models import Avg
from django.utils.timezone import now

from authentication.models import CustomUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',  # Self-referential foreign key
        on_delete=models.CASCADE,  # Delete subcategories if the parent is deleted
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shipping_addresses')
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)  # Mark as default address

    def __str__(self):
        return f"{self.full_name} - {self.address_line_1}, {self.city}, {self.country}"
class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)  # Unique discount code
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Discount percentage (e.g., 10.00 for 10%)
    valid_from = models.DateTimeField()  # Start date for the discount code
    valid_until = models.DateTimeField()  # End date for the discount code
    is_active = models.BooleanField(default=True)  # Whether the code is active

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"

    def is_valid(self):
        # Check if the discount code is active and within the valid date range
        return self.is_active and self.valid_from <= now() <= self.valid_until

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Field for product image
    specifications = models.JSONField(default=dict, blank=True)  # Requires Django 3.1+

    def __str__(self):
        return self.name


    def average_rating(self):
        # Calculate the average rating of the product's reviews
        return self.reviews.aggregate(average=Avg('rating'))['average'] or 0

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE)  # Assuming you're using a custom User model
    rating = models.PositiveIntegerField()  # Rating out of 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"