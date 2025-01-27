from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet


class CustomDefaultRouter(DefaultRouter):
    """Custom router to serve the root path directly."""

    def get_default_basename(self, viewset):
        return "orders"


# Use the custom router to remove the extra "order" prefix
router = CustomDefaultRouter()
router.register(r"", OrderViewSet, basename="order")  # Register without a prefix

urlpatterns = [
    path("", include(router.urls)),  # All routes served at the root
]
