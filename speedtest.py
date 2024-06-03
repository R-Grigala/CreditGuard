import time
from rest_framework.test import APITestCase

class SpeedTestCardAPITestCase(APITestCase):
    def test_speed_of_card_creation(self):
        start_time = time.time()
        # Generate 100 random card numbers and CCVs
        for _ in range(100):
            data = {
                'title': 'Test Card',
                'card_number': 'random_card_number',
                'ccv': 'random_ccv'
            }
            response = self.client.post('/your-api-endpoint/', data)
            # Check if the card was created successfully
            self.assertEqual(response.status_code, 201)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Total execution time: {execution_time} seconds")
