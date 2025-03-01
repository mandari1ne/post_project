from rest_framework.generics import ListAPIView
from . import serializers
from . import models

from rest_framework import filters

class UsersApiView(ListAPIView):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return models.CustomUser.objects.all()

class SubscriptionApiView(ListAPIView):
    serializer_class = serializers.SubscriptionSerializer

    def get_queryset(self):
        return models.Subscription.objects.all()
