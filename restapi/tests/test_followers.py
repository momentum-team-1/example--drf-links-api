from django.test import TestCase
from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status


# Create your tests here.
class TestFollowers(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        token = Token.objects.get(user=self.user1)
        self.user2 = User.objects.create(username='user2')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_can_follow_a_user(self):
        response = self.client.post("/api/followed/", {"user": "user2"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['followed_user_count'], 1)
        self.assertTrue(self.user2 in self.user1.followed_users.all())

    def test_can_unfollow_a_user(self):
        self.user1.followed_users.add(self.user2)

        response = self.client.delete(f"/api/followed/{self.user2.id}/",
                                      format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.user2 in self.user1.followed_users.all())
