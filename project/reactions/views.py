from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posts import models
from .models import Reaction

# Create your views here.

@login_required
def react_to_post(request, post_id, reaction_type):
    post = models.Post.objects.get(id=post_id)

    existing_reaction = post.reactions.filter(user=request.user).first()

    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            existing_reaction.delete()
        else:
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
    else:
        Reaction.objects.create(user=request.user, post=post, reaction_type=reaction_type)

    return redirect(request.META.get('HTTP_REFERER'))
