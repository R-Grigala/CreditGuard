from rest_framework.test import APITestCase
from django.contrib.auth.models import User

import time

class CardsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='new_user', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_valid_card_creation(self):
        # სწორი card_number-ისა და cvv-ის status_code
        data = {
            'card_number': '1122334455668888',
            'ccv': '103'
        }
        response = self.client.post('/cards/', data)
        self.assertEqual(response.status_code, 201)

    def test_invalid_card_creation(self):
        # არასწორი card_number-ის შეცდომის ნახვა
        data = {
            'card_number': '1122334455667788',
            'ccv': '103'
        }
        response = self.client.post('/cards/', data)
        self.assertEqual(response.status_code, 400)

        # არასწორი CVV-ის შეცდომის ნახვა
        data = {
            'card_number': '1122334455668888',
            'ccv': '1234'
        }
        response = self.client.post('/cards/', data)
        self.assertEqual(response.status_code, 400)


class CardsSpeedTestCase(APITestCase):
    def test_speed_of_card_creation(self):
        # ავტორიზაცია აუცილებელია card-ის დამატების დროს, ბაზების კავშირის გამო user(FK to user),
        self.user = User.objects.create_user(username='test_admin', password='password123')
        self.client.force_authenticate(user=self.user)

        start_time = time.time()
        # გავტესტოთ card -ის 100 მონაცემზე სისწრაფე
        for i in range(100):
            data = {
                'card_number': '1122334455668888',
                'ccv': '103'
            }
            response = self.client.post('/cards/', data)
            # თუ აბრუნებს status_code 201, მაშინ წარმატებით ემატება მონაცემები ბაზაში
            self.assertEqual(response.status_code, 201)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Total execution time: {execution_time} seconds")

