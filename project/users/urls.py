from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('api_users/', api.UsersApiView.as_view(), name='api_users'),
    path('api_subscriptions/', api.SubscriptionApiView.as_view(), name='api_subscriptions'),
    path('users/', views.user_index, name='user_index'),
    path('users/edit_profile/', views.edit_profile, name='edit_profile'),
    path('users/followers/', views.user_followers, name='followers_list'),
    path('users/subscriptions/', views.user_subscriptions, name='subscriptions_list'),
    path('users/follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('users/unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('users/profile/<int:user_id>/', views.view_user_profile, name='user_profile'),
    path('register/', views.register, name='register'),
]
