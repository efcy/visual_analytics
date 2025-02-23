from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from common.models import Event


class EventAPITests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.super_user = User.objects.create_superuser(username='jane', email='jane@doe.com', password='jane123')
        self.admin_token = Token.objects.get(user=self.super_user)
        print("run setup!!!!!!!!!!!")
        return super().setUp()

    def test_create_model(self):
        # FIXME why does reverse lookup not work here
        #url = "api" + reverse('events') + "/" # Use the URL name from your app's urls.py
        
        data = {'name': 'Test Event'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post('/api/events/', data, format='json')
        print(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().name, 'Test Event')