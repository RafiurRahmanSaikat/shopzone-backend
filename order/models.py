# Create your models here.
import uuid

from django.contrib.auth import get_user_model

User = get_user_model()
from django.db import models

from product.models import Product


# Order App Models
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        CANCELLED = "Cancelled"
        SHIPPED = "Shipped"
        DELIVERED = "Delivered"

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    products = models.ManyToManyField(Product, through="OrderProduct")

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    products = models.ManyToManyField(Product, through="CartItem")

    @property
    def item_subtotal(self):
        return sum(item.product.price * item.quantity for item in self.cart_items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
