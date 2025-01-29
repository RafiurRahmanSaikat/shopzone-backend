from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

User = get_user_model()

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import IsAdmin, IsOwner
from .serializers import (
    PasswordChangeSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        elif self.action == "destroy":
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    @action(detail=False, methods=["get", "put", "patch"])
    @method_decorator(cache_page(60 * 15))
    def me(self, request):
        if request.method in ["PUT", "PATCH"]:
            serializer = UserUpdateSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            request.user.clear_cache()  # Clear cache after update
            return Response(serializer.data)

        # Handle GET request
        cache_key = request.user.get_cache_key()
        data = cache.get(cache_key)

        if not data:
            serializer = self.get_serializer(request.user)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 15)

        return Response(data)

    @action(detail=False, methods=["post"])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.user.clear_cache()
        return Response({"detail": "Password changed successfully."})
