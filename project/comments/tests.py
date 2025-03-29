from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Comment
from posts.models import Post
from reactions.models import Reaction
from django.db.models import Count


# Create your tests here.


class CommentModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="password123"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="password123"
        )

        self.post = Post.objects.create(
            user=self.user1,
            category=None,
            text="Test post content."
        )

        self.comment = Comment.objects.create(
            user=self.user2,
            post=self.post,
            text="Test comment."
        )

    # создание комментария
    def test_comment_creation(self):
        self.assertEqual(self.comment.user.username, "user2")
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.text, "Test comment.")

    # счетчик лайков
    def test_likes_count_property(self):
        self.assertEqual(self.comment.likes_count, 0)

    # счетчик дизлайков
    def test_dislikes_count_property(self):
        self.assertEqual(self.comment.dislikes_count, 0)

    # добавление реакции
    def test_adding_reactions(self):
        reaction_like = Reaction.objects.create(
            user=self.user1,
            comment=self.comment,
            reaction_type='like'
        )
        reaction_dislike = Reaction.objects.create(
            user=self.user2,
            comment=self.comment,
            reaction_type='dislike'
        )

        self.assertEqual(self.comment.reactions_count, 2)
        self.assertEqual(self.comment.likes_count, 1)
        self.assertEqual(self.comment.dislikes_count, 1)
