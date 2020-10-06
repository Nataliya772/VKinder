import unittest
from unittest.mock import patch

from vk_api import BadPassword

import Get_token
import User

class TestAPI_User(unittest.TestCase):

    def test_fail_incorrect_data(self):
        with self.assertRaises(BadPassword):
            with patch('Get_token.input', side_effect = ['bfdvbl@mail.ru', 'bfuebu78ejhf']):
                Get_token.get_token()

    def setUp(self):
        TOKEN = '10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c'
        self.user = User.UserVK(TOKEN)

    def test_get_params(self):
        self.user.get_params()
        self.user.get_user_info()
        self.assertTrue(self.user.__dict__['user']['id'])

        def test_get_user_id(self):
            for value in self.user:
                v = value['id']
                self.get_user_id()
                self.assertEqual(v, self.user_id)

        def test_get_bdate_user(self):
            for value in self.user:
                v = value['bdate']
                self.get_bdate_user()
                self.assertNotEqual('0.0.0', self.bdate_user)
                self.assertTrue(self.age_user)

        def test_get_sex_user(self):
            for value in self.user:
                v = value['sex']
                self.get_sex_user()
                self.assertEqual(v, self.sex_user)
