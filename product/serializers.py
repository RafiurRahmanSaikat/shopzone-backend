from rest_framework import serializers

from product.models import Brand, Category, Product, Review


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "product",
            "user",
            "rating",
            "comment",
            "created_at",
        )


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    categories = CategorySerializer(many=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "rating",
            "is_approved",
            "image",
            "store",
            "brand",
            "categories",
            "reviews",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    categories = CategorySerializer(many=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "rating",
            "is_approved",
            "image",
            "store",
            "brand",
            "categories",
            "reviews",
        )


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
