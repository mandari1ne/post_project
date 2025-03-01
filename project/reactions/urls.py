from django.urls import path
# from . import views
from . import api

urlpatterns = [
    path('api_reactions/', api.ReactionApiView.as_view(), name='api_reactions'),
]
