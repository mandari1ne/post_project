from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, PostImage
from .forms import PostEditForm
from users import models
from reactions.models import Reaction


def post_index(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    posts = Post.annotate_post_data().prefetch_related('images')

    if category_id:
        posts = posts.filter(category_id=category_id)

    posts = posts.order_by('-created_at')

    # Получим реакции текущего пользователя (если он вошёл)
    user_reactions = {}
    if request.user.is_authenticated:
        reactions = Reaction.objects.filter(user=request.user, post__in=posts)
        user_reactions = {reaction.post_id: reaction.reaction_type for reaction in reactions}

    # Добавим реакцию к каждому посту
    for post in posts:
        post.user_reaction = user_reactions.get(post.id)

    return render(request, 'posts_index.html', {
        'categories': categories,
        'posts': posts,
    })


# def post_index(request):
#     categories = Category.objects.all()
#     category_id = request.GET.get('category')
#
#     posts = Post.annotate_post_data().prefetch_related('images')
#
#     if category_id:
#         posts = posts.filter(category_id=category_id)
#
#     posts = posts.order_by('-created_at')
#
#     return render(request, 'posts_index.html', {
#         'categories': categories,
#         'posts': posts,
#     })


def post_detail(request, pk):
    post = get_object_or_404(
        Post.annotate_post_data().prefetch_related('images'),
        pk=pk
    )

    return render(request, 'post_detail.html', {
        'post': post,
    })


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            if request.POST.get('delete_file') and post.file:
                post.file.delete(save=False)
                post.file = None

            post = form.save()

            delete_image_ids = request.POST.getlist('delete_images')
            if delete_image_ids:
                for image_id in delete_image_ids:
                    image = PostImage.objects.filter(id=image_id, post=post).first()
                    if image:
                        image.image.delete(save=False)
                        image.delete()

            images = request.FILES.getlist('images')
            for image in images:
                PostImage.objects.create(post=post, image=image)

            return redirect('post_index')

    else:
        form = PostEditForm(instance=post)

    form.fields['images'].widget.attrs['queryset'] = post.images.all()

    return render(request, 'post_edit.html', {'form': form, 'post': post})


def view_user_posts(request, user_id):
    target_user = get_object_or_404(models.CustomUser, id=user_id)

    categories = Category.objects.all()
    category_id = request.GET.get('category')

    posts = Post.annotate_post_data().filter(user=target_user).prefetch_related('images')

    if category_id:
        posts = posts.filter(category_id=category_id)

    posts = posts.order_by('-created_at')

    return render(request, 'user_posts.html', {
        'target_user': target_user,
        'categories': categories,
        'posts': posts,
        'selected_category': category_id,
    })
