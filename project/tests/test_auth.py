import json
from project.tests.base import BaseTestCase
import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_company

class TestAuthService(BaseTestCase):
    def test_user_registration(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'justatest',
                    'email': 'test@test.com',
                    'password': '123456',
                    'company_id': company.id
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        add_user('test', 'test@test.com', 'test', company.id)
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'test@test.com',
                    'password': 'test',
                    'company_id': company.id
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('fail', data['status'])
    def test_user_registration_duplicate_username(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        add_user('test', 'test@test.com', 'test', company.id)
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'test',
                    'email': 'test@test.com2',
                    'password': 'test',
                    'company_id': company.id
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('fail', data['status'])
    def test_user_registration_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test',
                    'company_id': company.id
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
    def test_user_registration_invalid_json_keys_no_email(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'justatest',
                    'password': 'test',
                    'company_id': company.id
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
    def test_user_registration_invalid_json_keys_no_password(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'justatest',
                    'email': 'test@test.com',
                    'company_id': company.id
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])