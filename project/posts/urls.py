from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('api_category/', api.CategoryApiView.as_view(), name='api_category'),
    path('api_posts/', api.PostsApiView.as_view(), name='api_posts'),
    path('api_post_image/', api.PostImangeApiView.as_view(), name='api_post_image'),
    path('posts/', views.post_index, name='post_index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
]
