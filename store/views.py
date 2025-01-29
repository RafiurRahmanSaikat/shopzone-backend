from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer
from product.models import Product
from product.serializers import ProductSerializer

from .models import Store, StoreCategory
from .permissions import IsOwnerOrAdmin
from .serializers import StoreCategorySerializer, StoreSerializer


class StoreCategoryViewSet(viewsets.ModelViewSet):
    queryset = StoreCategory.objects.all()
    serializer_class = StoreCategorySerializer
    permission_classes = [IsAuthenticated]

    def has_permission(self, request, view):
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return request.user.is_staff
        return True


class StoreViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Store.objects.all()
        return Store.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["get"])
    def products(self, request, pk=None):
        store = self.get_object()
        products = Product.objects.filter(store=store)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def orders(self, request, pk=None):
        store = self.get_object()
        orders = Order.objects.filter(order_products__product__store=store).distinct()

        # orders = Order.objects.filter(items__product__store=store).distinct()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
