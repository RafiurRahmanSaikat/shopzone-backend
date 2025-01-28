from rest_framework import viewsets

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("orderproduct_set__product", "user")
    serializer_class = OrderSerializer
