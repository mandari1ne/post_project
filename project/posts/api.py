from rest_framework.generics import ListAPIView
from . import serializers
from . import models

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class CategoryApiView(ListAPIView):
    serializer_class = serializers.CategorySerializer

    filter_backends = [filters.OrderingFilter]
    ordering_field = ['name']

    def get_queryset(self):
        return models.Category.objects.all()

class PostsApiView(ListAPIView):
    serializer_class = serializers.PostSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['category', 'created_at']

    def get_queryset(self):
        return models.Post.objects.all()

class PostImangeApiView(ListAPIView):
    serializer_class = serializers.PostImageSerializer

    def get_queryset(self):
        return models.PostImage.objects.all()
