import django_filters
from django.db.models import Q
from rest_framework import filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["iexact", "icontains"],
            "price": ["exact", "lt", "gt", "range"],
        }


class ProductPermissionFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user

        if user.is_authenticated:
            if user.is_staff:
                return queryset
            if user.role in ["store_owner", "admin"]:
                return queryset.filter(Q(store__owner=user) | Q(store__manager=user))

        # Regular users only see approved products
        return queryset
