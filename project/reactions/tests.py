from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment
from .models import Reaction


# Create your tests here.


class ReactionModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="password123")
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="password123")

        self.post = Post.objects.create(
            user=self.user1, category=None, text="Test post content.")
        self.comment = Comment.objects.create(
            user=self.user2, post=self.post, text="Test comment.")

    # создание реакции
    def test_reaction_creation(self):
        reaction = Reaction.objects.create(
            user=self.user1,
            post=self.post,
            reaction_type='like'
        )
        self.assertEqual(reaction.user, self.user1)
        self.assertEqual(reaction.post, self.post)
        self.assertEqual(reaction.reaction_type, 'like')
        self.assertIsNotNone(reaction.created_at)

    # уникальность реакции для поста
    def test_unique_reaction_for_post(self):
        Reaction.objects.create(
            user=self.user1, post=self.post, reaction_type='like')

        with self.assertRaises(Exception):
            Reaction.objects.create(
                user=self.user1, post=self.post, reaction_type='dislike')

    # уникальность реакции для комментария
    def test_unique_reaction_for_comment(self):
        Reaction.objects.create(
            user=self.user1, comment=self.comment, reaction_type='like')

        with self.assertRaises(Exception):
            Reaction.objects.create(
                user=self.user1, comment=self.comment, reaction_type='dislike')

    # создание двух одинаковых реакций
    def test_reaction_to_post_and_comment_with_constraints(self):
        Reaction.objects.create(
            user=self.user1, post=self.post, reaction_type='like')

        with self.assertRaises(Exception):
            Reaction.objects.create(
                user=self.user1, post=self.post, reaction_type='like')
