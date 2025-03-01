from django.db import models

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'Comment {self.id} by {self.user.username}'

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
    def annotate_comment_data(cls):
        return cls.objects.annotate(
            reactions_count=Count('reactions'),
            likes_count=Count(Case(When(reactions__reaction_type='like', then=1), output_field=IntegerField())),
            dislikes_count=Count(Case(When(reactions__reaction_type='dislike', then=1), output_field=IntegerField()))
        )
