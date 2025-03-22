from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from posts import models
from .forms import CommentForm
from .models import Comment


# Create your views here.


def post_comments(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)

    comments = (
        post.comments
        .select_related('user')
        .prefetch_related('replies__user')
        .filter(parent__isnull=True)
        .order_by('-created_at')
    )

    form = CommentForm()

    if request.user.is_authenticated:
        for comment in comments:
            comment.user_reaction = comment.reactions.filter(user=request.user).first()

            for reply in comment.replies.all():
                reply.user_reaction = reply.reactions.filter(user=request.user).first()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id, post=post).first()
                if parent_comment:
                    comment.parent = parent_comment

            comment.save()

            return redirect('post_comments', post_id=post_id)

    referer_url = request.META.get('HTTP_REFERER', '')

    if f'/posts/{post_id}' in referer_url:
        back = reverse('post_detail', args=[post_id])
    elif '/posts' in referer_url:
        back = reverse('post_index')
    else:
        back = reverse('post_index')

    return render(request, 'post_comments.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'back': back,
    })


@login_required
def comments_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post

    if request.method == 'POST':
        comment.delete()

    return redirect('post_comments', post_id=post.id)
