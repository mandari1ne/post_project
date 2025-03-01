from rest_framework.generics import ListAPIView
from . import serializers
from . import models

from rest_framework import filters

class ReactionApiView(ListAPIView):
    serializer_class = serializers.ReactionSerializer

    def get_queryset(self):
        return models.Reaction.objects.all()
