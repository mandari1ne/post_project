from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('api_reactions/', api.ReactionApiView.as_view(), name='api_reactions'),
    path('post/<int:post_id>/<str:reaction_type>/', views.react_to_post, name='react_to_post'),
]
