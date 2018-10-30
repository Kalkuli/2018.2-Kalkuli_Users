import json
import unittest
from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    
    def test_users(self):
        response = self.client.get('/')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to Kalkuli Users Service!!', data['data'])


    def test_add_company(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({

                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('Company was created!', data['message'])


        
if __name__ == '__main__':
    unittest.main()