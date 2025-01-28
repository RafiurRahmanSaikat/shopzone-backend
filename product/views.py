from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Brand, Category, Product, Review
from .permissions import IsAdmin, IsAdminOrStoreManagerOrOwner
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrStoreManagerOrOwner]

    def get_queryset(self):
        return Product.objects.all()

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

    @action(
        detail=True, methods=["post"], permission_classes=[IsAdminOrStoreManagerOrOwner]
    )
    def request_approval(self, request, pk=None):
        product = self.get_object()
        if product.is_approved:
            return Response(
                {"detail": "Product is already approved."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Logic to send approval request (e.g., notify admin)
        return Response({"detail": "Approval request sent."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        product = self.get_object()
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin can approve products."},
                status=status.HTTP_403_FORBIDDEN,
            )
        product.is_approved = True
        product.save()
        return Response({"detail": "Product approved."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def cancel_approval(self, request, pk=None):
        product = self.get_object()
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admin can cancel approvals."},
                status=status.HTTP_403_FORBIDDEN,
            )
        product.is_approved = False
        product.save()
        return Response(
            {"detail": "Product approval canceled."}, status=status.HTTP_200_OK
        )


class BrandViewSet(viewsets.ModelViewSet):

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrStoreManagerOrOwner]

    def has_permission(self, request, view):
        # Allow only admins
        return request.user.is_authenticated and request.user.role == "admin"


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStoreManagerOrOwner]

    def has_permission(self, request, view):
        # Allow only admins
        return request.user.is_authenticated and request.user.role == "admin"
