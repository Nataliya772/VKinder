import unittest
from unittest.mock import patch

from vk_api import BadPassword

import Get_token
import User

class TestAPI(unittest.TestCase):

    def test_fail_incorrect_data(self):
        with self.assertRaises(BadPassword):
            with patch('Get_token.input', side_effect = ['bfdvbl@mail.ru', 'bfuebu78ejhf']):
                Get_token.get_token()

    def test_API_connect(self):
        def setUp(self):
            TOKEN = '10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c'
            self.user = User.UserVK(TOKEN)

        def test_get_params(self):
            self.get_params()
            self.get_user_info()
            for value in self.user:
                v = value['id']
                self.assertTrue(v)



        #self.assertIn(dict, str(User.UserVK.get_params(self)))
        #self.assertIn('200', str(User.UserVK.get_user_info(self)))