from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from order.serializers import CartSerializer, OrderSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    # cart = CartSerializer(read_only=True)
    # orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "get_full_name",
            "role",
            # "email",
            # "is_authenticated",
            # "orders",
            # "cart",
        )


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
        # Hash the password
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "address", "profile_picture")


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        # Add password validation logic if needed
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
