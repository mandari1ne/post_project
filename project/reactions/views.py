from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posts import models
from .models import Reaction
from comments.models import Comment


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


@login_required
def post_reactions_view(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)

    likes = Reaction.objects.filter(post=post, reaction_type='like').select_related('user')
    dislikes = Reaction.objects.filter(post=post, reaction_type='dislike').select_related('user')

    return render(request, 'post_reactions.html', {
        'post': post,
        'likes': likes,
        'dislikes': dislikes
    })

@login_required
def react_to_comment(request, comment_id, reaction_type):
    comment = get_object_or_404(Comment, id=comment_id)

    existing_reaction = comment.reactions.filter(user=request.user).first()

    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            existing_reaction.delete()
        else:
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
    else:
        Reaction.objects.create(user=request.user, comment=comment, reaction_type=reaction_type)

    return redirect(request.META.get('HTTP_REFERER'))
