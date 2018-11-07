import json
from project.tests.base import BaseTestCase
import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_company
from flask import current_app

class TestAuthService(BaseTestCase):
    def test_user_registration(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'company_name': 'Kalkuli',
                    'cnpj': '00.000.000/0000-00',
                    'company_email': 'contact.kalkuli@kalkuli.com',
                    'fantasy_name': 'Kaliu',
                    'cep': '00-000/00',
                    'city': 'Brasilia',
                    'state': 'Distrito Federal',
                    'company_phone': '61 98888888',
                    'username': 'justatest',
                    'email': 'test@test.com',
                    'password': '12345678'
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
                    'company_name': 'Kalkuli',
                    'cnpj': '00.000.000/0000-00',
                    'company_email': 'contact.kalkuli@kalkuli.com',
                    'fantasy_name': 'Kaliu',
                    'cep': '00-000/00',
                    'city': 'Brasilia',
                    'state': 'Distrito Federal',
                    'company_phone': '61 98888888',
                    'username': 'michael',
                    'email': 'test@test.com',
                    'password': 'test',
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

    def test_registered_user_login(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        with self.client:
            add_user('test', 'test@test.com', 'test', company.id)
            response = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test',
                    'company_id': company.id
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_valid_logout(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        add_user('test', 'test@test.com', 'test', company.id)
        with self.client:
            # user login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test',
                    'company_id': company.id
                }),
                content_type='application/json'
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        add_user('test', 'test@test.com', 'test', company.id)
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test',
                    'company_id': company.id
                }),
                content_type='application/json'
            )
            # invalid token logout
            time.sleep(4)
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
            data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': 'Bearer invalid'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
            data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_expired_token(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        add_user('test', 'test@test.com', 'test', company.id)
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            # invalid token logout
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_inactive(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        add_user('test', 'test@test.com', 'test', company.id)
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                 }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        add_user('test', 'test@test.com', 'test', company.id)
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'test')
            self.assertTrue(data['data']['email'] == 'test@test.com')
            self.assertTrue(data['data']['active'] is True)
            self.assertEqual(response.status_code, 200)
    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': 'Bearer invalid'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
            data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_status_inactive(self):
        company = add_company('Kalkuli', '00.000.000/0000-00', 'kalkuli@kaliu.com', 'kaliu', '789548546', 'ceilandia', 'df', '40028922')
        add_user('test', 'test@test.com', 'test', company.id)
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 401)