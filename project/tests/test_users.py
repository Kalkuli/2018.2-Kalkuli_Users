import json
import unittest
from project.tests.base import BaseTestCase
from project import db
from sqlalchemy.exc import IntegrityError
from project.tests.utils import add_user, add_company
from project.api.models import User, Company


class TestUserService(BaseTestCase):
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