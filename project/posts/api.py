from rest_framework.generics import ListAPIView
from . import serializers
from . import models

from rest_framework import filters

class CategoryApiView(ListAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return models.Category.objects.all()

class PostsApiView(ListAPIView):
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        return models.Post.objects.all()

class PostImangeApiView(ListAPIView):
    serializer_class = serializers.PostImageSerializer

    def get_queryset(self):
        return models.PostImage.objects.all()
