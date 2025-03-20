from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posts import models
from .models import Reaction

# Create your views here.

@login_required
def react_to_post(request, post_id, reaction_type):
    post = models.Post.objects.get(id=post_id)

    # Проверяем, существует ли уже реакция этого пользователя на данный пост
    existing_reaction = post.reactions.filter(user=request.user).first()

    # Если реакция существует и она такая же, удаляем её
    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            existing_reaction.delete()
        else:
            # Если реакция не такая же, обновляем её на новую
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
    else:
        # Если реакции нет, создаем новую
        Reaction.objects.create(user=request.user, post=post, reaction_type=reaction_type)

    return redirect(request.META.get('HTTP_REFERER'))
