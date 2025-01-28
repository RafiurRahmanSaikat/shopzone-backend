from django.db import transaction
from rest_framework import serializers

from order.models import Cart, CartItem, Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_image = serializers.CharField(source="product.image", read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price", read_only=True
    )
    item_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = (
            "product_name",
            "product_price",
            "product_image",
            "quantity",
            "item_subtotal",
        )

    def get_item_subtotal(self, obj):
        return obj.product.price * obj.quantity


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderProductCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderProduct
            fields = ("product", "quantity")

    order_id = serializers.UUIDField(read_only=True)
    products = OrderProductCreateSerializer(many=True, write_only=True)

    def create(self, validated_data):
        # Debug: Print the validated data and request user
        print("Validated Data:", validated_data)
        print("Request User:", self.context["request"].user)

        # Automatically set the user to the currently logged-in user
        validated_data["user"] = self.context["request"].user
        products_data = validated_data.pop("products", [])

        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for product_data in products_data:
                OrderProduct.objects.create(order=order, **product_data)

        return order

    class Meta:
        model = Order
        fields = ("order_id", "user", "status", "products")
        extra_kwargs = {"user": {"read_only": True}}


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(
        source="orderproduct_set", many=True, read_only=True
    )
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return sum(
            item.product.price * item.quantity for item in obj.orderproduct_set.all()
        )

    class Meta:
        model = Order
        fields = ("order_id", "created_at", "user", "status", "products", "total_price")


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ("id", "product", "product_name", "product_price", "quantity")


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    item_subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = ("id", "cart_items", "item_subtotal")
