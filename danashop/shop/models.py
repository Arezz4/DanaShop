from django.db import models
from django.db.models import Avg

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
        db_table = 'categories'
        verbose_name_plural = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Field for product image
    specifications = models.JSONField(default=dict, blank=True)  # Requires Django 3.1+

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name


    def average_rating(self):
        # Calculate the average rating of the product's reviews
        return self.reviews.aggregate(average=Avg('rating'))['average'] or 0


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE)  # Assuming you're using a custom User model
    rating = models.PositiveIntegerField()  # Rating out of 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"