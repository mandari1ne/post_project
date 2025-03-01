from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class CustomUser(AbstractUser):
    icon = models.ImageField(upload_to='user_icons/', blank=True, null=True)
    level = models.PositiveIntegerField(default=1)
    subscriptions = models.ManyToManyField("self",
                                            symmetrical=False,
                                            related_name="followers",
                                            blank=True,
                                            through='Subscription',
                                            help_text="Users that this user is subscribed to.")
    date_joined = models.DateTimeField(default=now)

    def __str__(self):
        return self.username

class Subscription(models.Model):
    subscriber = models.ForeignKey(
        'CustomUser', related_name='subscriptions_set', on_delete=models.CASCADE
    )
    subscribed_user = models.ForeignKey(
        'CustomUser', related_name='subscribed_by_set', on_delete=models.CASCADE
    )
    date_subscribed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_user')

    def __str__(self):
        return f"{self.subscriber.username} subscribed to {self.subscribed_user.username}"

