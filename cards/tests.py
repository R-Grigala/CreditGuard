from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class CardAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_valid_card_creation(self):
        data = {
            'title': 'Test Card',
            'card_number': '1234567890123456',
            'ccv': '123'
        }
        response = self.client.post('/your-api-endpoint/', data)
        self.assertEqual(response.status_code, 201)

    def test_invalid_card_creation(self):
        # Test with invalid card number
        data = {
            'title': 'Test Card',
            'card_number': 'invalid_card_number',
            'ccv': '123'
        }
        response = self.client.post('/your-api-endpoint/', data)
        self.assertEqual(response.status_code, 400)

        # Test with invalid CCV
        data = {
            'title': 'Test Card',
            'card_number': '1234567890123456',
            'ccv': 'invalid_ccv'
        }
        response = self.client.post('/your-api-endpoint/', data)
        self.assertEqual(response.status_code, 400)
