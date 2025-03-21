from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('api_comments/', api.CommentsApiView.as_view(), name='api_comments'),
    path('post/<int:post_id>/comments/', views.post_comments, name='post_comments'),
]
