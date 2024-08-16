from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import organization
#not working
User = get_user_model()

class AuthViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.check_auth_url = reverse('authenticated')
        self.csrf_url = reverse('csrf_cookie')

        # Create a test organization
        self.test_org = organization.objects.create(name='Test Org')

    def test_signup(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            're_password': 'testpass123',
            'name': 'Test User',
            'first_name': 'Test',
            'email': 'test@example.com',
            'organization': 'Test Org'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'success': 'User created successfully'})
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login(self):
        # Create a user first
        User.objects.create_user(username='testuser', password='testpass123', orga=self.test_org)
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'success': 'User authenticated'})

    def test_logout(self):
        # Create and login a user first
        user = User.objects.create_user(username='testuser', password='testpass123', orga=self.test_org)
        self.client.force_authenticate(user=user)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'success': 'Loggout Out'})

    def test_check_authenticated(self):
        # Test unauthenticated user
        response = self.client.get(self.check_auth_url)
        self.assertEqual(response.data, {'isAuthenticated': 'error'})

        # Test authenticated user
        user = User.objects.create_user(username='testuser', password='testpass123', orga=self.test_org)
        self.client.force_authenticate(user=user)
        response = self.client.get(self.check_auth_url)
        self.assertEqual(response.data, {'isAuthenticated': 'success'})

    def test_get_csrf_token(self):
        response = self.client.get(self.csrf_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'success': 'CSRF cookie set'})