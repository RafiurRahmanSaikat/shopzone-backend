from rest_framework import permissions, viewsets

from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("orderproduct_set__product", "user")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Order.objects.prefetch_related("orderproduct_set__product", "user")
        if user.role == "customer":
            return Order.objects.filter(user=user).prefetch_related(
                "orderproduct_set__product", "user"
            )
