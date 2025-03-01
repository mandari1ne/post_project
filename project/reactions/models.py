from django.db import models

# Create your models here.

class Reaction(models.Model):
    REACTION_TYPE = [
        ('like', 'Like'),
        ('dislike', 'Dislike')
    ]

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='reactions'
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reactions'
    )
    comment = models.ForeignKey(
        'comments.Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reactions'
    )
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_post_reaction'),
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_comment_reaction'),
        ]

    def __str__(self):
        return f'{self.reaction_type} by {self.user.username}'

