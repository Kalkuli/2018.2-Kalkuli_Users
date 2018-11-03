import json
import unittest
from project.tests.base import BaseTestCase
from project import db
from sqlalchemy.exc import IntegrityError
from project.tests.utils import add_user



# def test_users(self):
#     response = self.client.get('/')
#     data = json.loads(response.data.decode())
#     self.assertEqual(response.status_code, 200)
#     self.assertIn('Welcome to Kalkuli Users Service!!', data['data'])

class TestUserService(BaseTestCase):
    def test_add_company(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli',
                        'cnpj': '00.000.000/0000-00',
                        'company_email': 'contact.kalkuli@kalkuli.com',
                        'fantasy_name': 'Kaliu',
                        'cep': '00-000/00',
                        'city': 'Brasilia',
                        'state': 'Distrito Federal',
                        'company_phone': '61 98888888'
                    },
                    'user': {
                        'name': 'Esio',
                        'email': 'esiogustavo@kalkuli.com',
                        'password': 'xxxsxsxs'
                    }
                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('Company was created!', data['message'])

    def test_add_company_only_not_nullable(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli',
                        'company_email': 'contact.kalkuli@kalkuli.com'
                    },
                    'user': {
                        'name': 'Esio',
                        'email': 'esiogustavo@kalkuli.com',
                        'password': 'xxxsxsxs'
                    }
                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('Company was created!', data['message'])

    def test_add_company_empty_json(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({}), 
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('company could not be saved', data['message'])

    def test_add_company_missing_user(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli',
                        'cnpj': '00.000.000/0000-00',
                        'company_email': 'contact.kalkuli@kalkuli.com',
                        'fantasy_name': 'Kaliu',
                        'cep': '00-000/00',
                        'city': 'Brasilia',
                        'state': 'Distrito Federal',
                        'company_phone': '61 98888888'
                    },
                    'user': {
                    }
                }), 
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('company could not be saved', data['message'])

    def test_add_company_missing_company(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({
                    'company': {
                    },
                    'user': {
                        'name': 'Esio',
                        'email': 'esiogustavo@kalkuli.com',
                        'password': 'xxxsxsxs'
                    }
                }), 
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('company could not be saved', data['message'])

    def test_add_company_missing_company_name(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({
                    'company': {
                        'company_email': 'contact.kalkuli@kalkuli.com'
                    },
                    'user': {
                        'name': 'Esio',
                        'email': 'esiogustavo@kalkuli.com',
                        'password': 'xxxsxsxs'
                    }
                }), 
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('company could not be saved', data['message'])

    def test_add_company_missing_company_email(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli'
                    },
                    'user': {
                        'name': 'Esio',
                        'email': 'esiogustavo@kalkuli.com',
                        'password': 'xxxsxsxs'
                    }
                }), 
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('company could not be saved', data['message'])

    def test_add_company_missing_user_name(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli',
                        'company_email': 'contact.kalkuli@kalkuli.com'
                    },
                    'user': {
                        'email': 'esiogustavo@kalkuli.com',
                        'password': 'xxxsxsxs'
                    }
                }), 
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('company could not be saved', data['message'])

    def test_add_company_missing_user_email(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli',
                        'company_email': 'contact.kalkuli@kalkuli.com'
                    },
                    'user': {
                        'name': 'Esio',
                        'password': 'xxxsxsxs'
                    }
                }), 
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('company could not be saved', data['message'])

    def test_add_company_missing_user_password(self):
        with self.client:
            response = self.client.post(
                '/add_company',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli',
                        'company_email': 'contact.kalkuli@kalkuli.com'
                    },
                    'user': {
                        'name': 'Esio',
                        'email': 'esiogustavo@kalkuli.com'
                    }
                }), 
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('company could not be saved', data['message'])

    def test_add_user(self):
        user = add_user('dutra', 'test@test.com', 'fasdudhusfa')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'dutra')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_email(self):
        user = add_user('dutra', 'test@test.com', 'sdfuhdhaus')
        db.session.add(user)
        db.session.commit()
        duplicate_user = add_user('lucas', 'test@test.com', 'ahudfhausdf')
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('dutra', 'test@test.com', 'greaterthaneight')
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user('dutra', 'test@test.com', 'greaterthaneight')
        user_two = add_user('lucas', 'test@test2.com', 'greaterthaneight')
        self.assertNotEqual(user_one.password, user_two.password)
        
if __name__ == '__main__':
    unittest.main()