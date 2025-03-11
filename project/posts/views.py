from django.shortcuts import render, get_object_or_404
from .models import Post, Category

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

