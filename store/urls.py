from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import StoreViewSet

router = DefaultRouter()
router.register(r"store", StoreViewSet, basename="store")

urlpatterns = [
    path("", include(router.urls)),
]
