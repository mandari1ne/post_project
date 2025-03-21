from django.db import models
from django.db.models import Count, Case, When, IntegerField, Q


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    text = models.TextField()
    file = models.FileField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.id} by {self.user.username}'

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def reactions_count(self):
        return self.reactions.count()

    @property
    def likes_count(self):
        return self.reactions.filter(reaction_type='like').count()

    @property
    def dislikes_count(self):
        return self.reactions.filter(reaction_type='dislike').count()

    @classmethod
    def annotate_post_data(cls):
        return cls.objects.annotate(
            comments_count_annotated=Count('comments', distinct=True),
            likes_count_annotated=Count('reactions', filter=Q(reactions__reaction_type='like'), distinct=True),
            dislikes_count_annotated=Count('reactions', filter=Q(reactions__reaction_type='dislike'), distinct=True),
            reactions_count_annotated=Count('reactions', distinct=True),
        )


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

    class Meta:
        indexes = [
            models.Index(fields=['post']),
        ]

    def __str__(self):
        return f'Image {self.id} for Post {self.post.id}'
