from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import InStockFilterBackend, ProductFilter
from .models import Product
from .serializers import ProductInfoSerializer, ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = (
        Product.objects.select_related("brand", "store")
        .prefetch_related("categories", "reviews")
        .order_by("pk")
    )
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
    ]
    search_fields = ["=name", "description"]
    ordering_fields = ["name", "price", "stock"]
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("brand", "store").prefetch_related(
        "categories", "reviews"
    )
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ProductInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        product_count = products.count()
        max_price = products.aggregate(max_price=Max("price"))["max_price"]

        serializer = ProductInfoSerializer(
            {"products": products, "count": product_count, "max_price": max_price}
        )
        return Response(serializer.data)
