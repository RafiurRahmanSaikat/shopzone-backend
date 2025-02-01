from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Brand, Category, Product, Review
from .permissions import IsAdminOrStoreOwner
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrStoreOwner]

    def get_queryset(self):
        # return Product.objects.all()
        return (
            Product.objects.all()
            .order_by("id")
            .select_related("brand", "store")
            .prefetch_related("categories", "reviews__user")
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="add_review",
    )
    def add_review(self, request, pk=None):
        product = self.get_object()
        user = request.user
        data = request.data

        # Check if user already reviewed
        if Review.objects.filter(product=product, user=user).exists():
            return Response(
                {"detail": "You have already reviewed this product."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and save review
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save(product=product, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ModelViewSet):

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrStoreOwner]

    def has_permission(self, request, view):
        # Allow only admins
        return request.user.is_authenticated and request.user.role == "admin"


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStoreOwner]

    def has_permission(self, request, view):
        # Allow only admins
        return request.user.is_authenticated and request.user.role == "admin"
