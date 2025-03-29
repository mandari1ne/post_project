from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Subscription
from django.utils import timezone


# Create your tests here.


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1",
            password="password123"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2",
            password="password123"
        )

    # на добавление нового пользователя
    def test_user_creation(self):
        self.assertEqual(self.user1.username, "user1")
        self.assertEqual(self.user2.username, "user2")
        self.assertTrue(self.user1.check_password("password123"))
        self.assertTrue(self.user2.check_password("password123"))

    # на создание подписки
    def test_subscription_creation(self):
        subscription = Subscription.objects.create(
            subscriber=self.user1,
            subscribed_user=self.user2
        )
        self.assertEqual(subscription.subscriber, self.user1)
        self.assertEqual(subscription.subscribed_user, self.user2)

    # на уникальность подписки
    def test_subscription_unique_together(self):
        Subscription.objects.create(subscriber=self.user1, subscribed_user=self.user2)

        with self.assertRaises(Exception):
            Subscription.objects.create(subscriber=self.user1, subscribed_user=self.user2)

    # на корректное отображение подписок
    def test_user_subscriptions(self):
        self.user1.subscriptions.add(self.user2)
        self.assertIn(self.user2, self.user1.subscriptions.all())
        self.assertIn(self.user1, self.user2.followers.all())
