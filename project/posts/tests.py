from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Post, PostImage
from django.db.models import Count


# Create your tests here.


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    # создание категории
    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")


class PostModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="user1", password="password123")
        self.category = Category.objects.create(name="Test Category")
        self.post = Post.objects.create(user=self.user, category=self.category, text="Test post content.")

    # создание поста
    def test_post_creation(self):
        self.assertEqual(self.post.user.username, "user1")
        self.assertEqual(self.post.category.name, "Test Category")
        self.assertEqual(self.post.text, "Test post content.")

    # счетчик комментариев
    def test_comments_count_property(self):
        self.assertEqual(self.post.comments_count, 0)

    # счетчик лайков
    def test_likes_count_property(self):
        self.assertEqual(self.post.likes_count, 0)

    # счетчик дизлайков
    def test_dislikes_count_property(self):
        self.assertEqual(self.post.dislikes_count, 0)


class PostImageModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="password123"
        )
        self.category = Category.objects.create(
            name="Test Category"
        )
        self.post = Post.objects.create(
            user=self.user,
            category=self.category,
            text="Test post content."
        )
        self.image = PostImage.objects.create(
            post=self.post,
            image="path/to/image.jpg"
        )

    # создание изображения для поста
    def test_post_image_creation(self):
        self.assertEqual(self.image.post, self.post)
        self.assertEqual(self.image.image, "path/to/image.jpg")
