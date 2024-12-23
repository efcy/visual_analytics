from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class PermissionTest(APITestCase):
    """test for the IsBerlinUnitedOrReadOnly permission class
        following https://www.django-rest-framework.org/api-guide/testing/
        """
    def setUp(self):
        self.event_url = '/api/events/' 
        return super().setUp()
    
    def test_no_user(self):     
        response = self.client.get(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {'detail': 'Authentication credentials were not provided.'}
        )

    def test_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+'642bcac87fd25e8719d48cf144e13653fb015ae')
        response = self.client.get(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {"detail": "Invalid token."}
        )

    def test_wrong_password(self):
        pass

    def test_get_w_token(self):
        pass

    def test_get_w_password(self):
        user = User.objects.create_user(username='john', email='js@js.com', password='js.sj')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.get(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_normal_user(self):
        pass

    def test_post_berlin_user(self):
        pass