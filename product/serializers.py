from rest_framework import serializers

from .models import Brand, Category, Product, Review, Store


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("id", "name")


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "product", "user", "rating", "comment", "created_at")
        read_only_fields = ("product", "user", "created_at")

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    store = StoreSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), write_only=True, source="brand"
    )
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True, source="categories"
    )
    store_id = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(), write_only=True, source="store"
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "description",
            "image",
            "stock",
            "categories",
            "rating",
            "reviews",
            "brand",
            "store",
            "brand_id",
            "category_ids",
            "store_id",
        )
        read_only_fields = ["rating"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    def validate(self, data):
        request = self.context.get("request")
        print(request, "request")

        # Allow all users to create/update products if they are admin
        if request and request.user:
            # Check if the user is an admin
            if request.user.role in ("admin", "store_owner"):
                return data

            # For non-admin users, check store permissions
            store = data.get("store")
            print(store, "store")

            # Ensure the store exists in the data
            if store:
                # Allow store owner or store manager to create/update products for their store
                if store.owner == request.user:
                    return data

                # If the user is neither the owner nor the manager, raise a validation error
                raise serializers.ValidationError(
                    {
                        "store_id": "You don't have permission to create/update products for this store."
                    }
                )

        print(data, "data")
        return data
