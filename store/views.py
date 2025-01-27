from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .models import Store
from .serializers import storeerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = storeerializer
