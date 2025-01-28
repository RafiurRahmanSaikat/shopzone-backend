from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("store_owner", "Store Owner"),
        ("admin", "Admin"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.username
