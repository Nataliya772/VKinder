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


    def test_get_user_id(self):
        self.user.get_user_id()
        self.assertEqual(self.user.user['id'], self.user.user_id)

    def test_get_bdate_user(self):
        self.user.get_bdate_user()
        self.assertNotEqual('0.0.0', self.user.bdate_user)

    def test_get_age_user(self):
        self.user.get_bdate_user()
        self.user.get_age_user()
        self.assertTrue(self.user.age_user)

    def test_get_sex_user(self):
        self.user.get_sex_user()
        self.assertEqual(self.user.user['sex'], self.user.sex_user)
