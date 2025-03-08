from django.shortcuts import render
from .models import Post, PostImage, Category

# Create your views here.

def post_index(request):
    categories = Category.objects.all()
    posts = Post.annotate_post_data().prefetch_related('images').order_by('-created_at')

    return render(request, 'posts_index.html', {
        'categories': categories,
        'posts': posts,
    })

