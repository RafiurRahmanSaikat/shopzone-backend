from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Store, StoreCategory


class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreCategory
        fields = ("id", "name")


class storeerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    store_categories = StoreCategorySerializer(many=True)

    class Meta:
        model = Store
        fields = ("id", "name", "address", "location", "owner", "store_categories")
