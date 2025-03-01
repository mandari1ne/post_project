from rest_framework.generics import ListAPIView
from . import serializers
from . import models

from rest_framework import filters

class CommentsApiView(ListAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.all()
