from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('api_users/', api.UsersApiView.as_view(), name='api_users'),
    path('api_subscriptions/', api.SubscriptionApiView.as_view(), name='api_subscriptions'),
    path('users/', views.users_index, name='user_index'),
]
