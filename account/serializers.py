from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from order.serializers import CartSerializer, OrderSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "get_full_name",
            "role",
            "email",
            "is_authenticated",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get("include_related"):
            data["orders"] = OrderSerializer(
                instance.orders.select_related("user").prefetch_related(
                    "order_products__product"
                ),
                many=True,
            ).data
            data["cart"] = CartSerializer(
                instance.cart.prefetch_related("cart_items__product")
            ).data
        return data


from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "phone_number",
            "address",
            "profile_picture",
            "role",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "address",
            "profile_picture",
        )


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "The two password fields didn't match."}
            )

        # Verify old password
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Current password is not correct"}
            )

        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
