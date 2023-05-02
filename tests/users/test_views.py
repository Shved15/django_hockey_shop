import random
import string
from datetime import timedelta
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.forms import UserProfileForm
from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'John',
            'last_name': 'Brezek',
            'username': 'johnbrezek',
            'email': 'johnbrezek@gmail.com',
            'password1': 'Password.1',
            'password2': 'Password.1',
        }
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Shop - Registration')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        # check the user does not exist
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        print(email_verification)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        user = User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'A user with that username already exists.', html=True)


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.username = 'john.doe'
        self.password = 'password123'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            email='john.doe@example.com'
        )

    # check that the login page loads successfully on a GET request.
    def test_user_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    # check that a successful user login redirects to the site's home page,
    # and that the user logs in correctly, i.e. that after logging in, the user is authenticated.
    def test_user_login_post_success(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # check that an invalid user login produces an error that is displayed on the login page.
    def test_user_login_post_error(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('Please enter a correct', response.content.decode())


# for generating a random username and email address
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


class UserProfileViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name='testname1',
            last_name='lastname1',
            username=generate_random_string(10),
            email=generate_random_string(10) + '@test.com',
            password='testpassword'
        )
        self.client = Client()
        self.client.login(username=self.user.username, password='testpassword')

    # checks that the profile page is displayed correctly and contains information about the user,
    # and that the correct template is used.
    def test_user_profile_view_success(self):
        response = self.client.get(reverse('users:profile', args=(self.user.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, self.user.username)

    # tests the user profile form, If the form passed the validation check, then the form.save() method is called.
    def test_user_profile_form_success(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': generate_random_string(10),
            'email': generate_random_string(10) + '@test.com',
            'image': SimpleUploadedFile('test_image.jpg', b''),
        }
        form = UserProfileForm(data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertIsNotNone(self.user.image)

    # checks that when filling out a profile form with invalid data,
    # the code 200 is returned and validation error messages are displayed.
    def test_user_profile_form_failure(self):
        data = {
            'first_name': '',
            'last_name': 'Fail',
            'image': SimpleUploadedFile('test_image.jpg', b''),
        }
        form = UserProfileForm(data, instance=self.user)
        self.assertFalse(form.is_valid())
        response = self.client.post(reverse('users:profile', args=(self.user.id,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
