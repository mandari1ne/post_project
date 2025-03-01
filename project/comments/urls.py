from django.urls import path
# from . import views
from . import api

urlpatterns = [
    path('api_comments/', api.CommentsApiView.as_view(), name='api_comments'),
]
