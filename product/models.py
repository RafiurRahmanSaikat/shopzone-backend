from django.db import models

from account.models import User
from store.models import Store


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    rating = models.FloatField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
