import json
import unittest
from project.tests.base import BaseTestCase
from project import db
from sqlalchemy.exc import IntegrityError
from project.tests.utils import add_user, add_company
from project.api.models import User, Company


class TestUserService(BaseTestCase):
    def test_add_company(self):
        with self.client:
            response = self.client.post(
                '/user',
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
                        'username': 'Esio',
                        'email': 'esiogustavo@kalkuli.com',
                        'password': 'xxxsxsxs'
                    }
                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('Company and user were created!', data['message'])

    def test_add_company_only_not_nullable(self):
        with self.client:
            response = self.client.post(
                '/user',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli',
                        'company_email': 'contact.kalkuli@kalkuli.com'
                    },
                    'user': {
                        'username': 'Esio',
                        'email': 'esiogustavo@kalkuli.com',
                        'password': 'xxxsxsxs'
                    }
                }),
                content_type = 'application/json',
            )

            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('Company and user were created!', data['message'])

    def test_all_users(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'k@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        company_two = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        add_user('michael', 'michael@mherman.org','pawwrerqew', company.id)
        add_user('fletcher', 'fletcher@notreal.com', 'sdhfudfs', company_two.id)
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('michael', data['data']['users'][0]['username'])
            self.assertIn('michael@mherman.org', data['data']['users'][0]['email'])
            self.assertIn('fletcher', data['data']['users'][1]['username'])
            self.assertIn(
            'fletcher@notreal.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_add_company_empty_json(self):
        with self.client:
            response = self.client.post(
                '/user',
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
                '/user',
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
                '/user',
                data = json.dumps({
                    'company': {
                    },
                    'user': {
                        'username': 'Esio',
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
                '/user',
                data = json.dumps({
                    'company': {
                        'company_email': 'contact.kalkuli@kalkuli.com'
                    },
                    'user': {
                        'username': 'Esio',
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
                '/user',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli'
                    },
                    'user': {
                        'username': 'Esio',
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

    def test_add_company_missing_username(self):
        with self.client:
            response = self.client.post(
                '/user',
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
                '/user',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli',
                        'company_email': 'contact.kalkuli@kalkuli.com'
                    },
                    'user': {
                        'username': 'Esio',
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
                '/user',
                data = json.dumps({
                    'company': {
                        'company_name': 'Kalkuli',
                        'company_email': 'contact.kalkuli@kalkuli.com'
                    },
                    'user': {
                        'username': 'Esio',
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
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        user = add_user('dutra', 'test@test.com', 'test', company.id)
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'dutra')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)
        self.assertEqual(user.company_id, company.id)

    def test_to_json(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        user = add_user('dutra', 'test@test.com', 'greaterthaneight', company.id)
        db.session.add(user)
        db.session.commit()
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kali@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        user_one = add_user('dutra', 'test@test.com', 'greaterthaneight', company.id)
        company_two = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        user_two = add_user('lucas', 'test@test2.com', 'greaterthaneight', company_two.id)
        self.assertNotEqual(user_one.password, user_two.password)

    def test_add_user_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                '/user',
                data=json.dumps({
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
                        'username': 'Esio',
                        'email': 'esiogustavo@kalkuli.com'
                    }
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('company could not be saved', data['message'])
            self.assertIn('fail', data['status'])

    def test_encode_auth_token(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        user = add_user('dutra', 'test@test.com', 'test', company.id)
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        user = add_user('dutra', 'test@test.com', 'test', company.id)
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token), user.id)

if __name__ == '__main__':
    unittest.main()