from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, PostImage
from .forms import PostEditForm


def post_index(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    posts = Post.annotate_post_data().prefetch_related('images')

    if category_id:
        posts = posts.filter(category_id=category_id)

    posts = posts.order_by('-created_at')

    return render(request, 'posts_index.html', {
        'categories': categories,
        'posts': posts,
    })


def post_detail(request, pk):
    post = get_object_or_404(
        Post.annotate_post_data().prefetch_related('images'),
        pk=pk
    )

    return render(request, 'post_detail.html', {'post': post})


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
