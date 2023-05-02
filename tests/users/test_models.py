from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTestCase(TestCase):
    """Test case for the User model."""

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
            'is_verified_email': True,
        }

    def test_create_user(self):
        """Test creating a new user."""
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.is_verified_email)

    def test_create_superuser(self):
        """Test creating a new superuser."""
        User = get_user_model()
        superuser = User.objects.create_superuser(**self.user_data)
        self.assertEqual(superuser.username, self.user_data['username'])
        self.assertEqual(superuser.email, self.user_data['email'])
        self.assertTrue(superuser.is_verified_email)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_str(self):
        """Test the string representation of a user."""
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['username'])
