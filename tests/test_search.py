import unittest
from unittest.mock import patch

import Search


class TestSearch(unittest.TestCase):

    def test_Search(self):
        def setUp(self):
            TOKEN = '10b2e6b1a90a01875cfaa0d2dd307b7a73a15ceb1acf0c0f2a9e9c586f3b597815652e5c28ed8a1baf13c'
            self.search = Search.SearchUsersVK()

        def test_get_user(self):
            self._get_user()
            for user in self._user:
                u = user['bdate_user']
                self.assertNotEqual(u, '0.0.0')

        def test_get_params_for_search(self):
            self._get_user()
            for user in self._user:
                u = user['sex_user']
                ua = user['age_user'] - 3
                self.get_params_for_search()
                s = self.get_params_for_search()['sex']
                usf = self.get_params_for_search()['age_from']
                self.assertNotEqual(u, s)
                self.assertEqual(ua, usf)

        def test_get_selected_users(self):
            for user in self.get_selected_users():
                l = user['link']
                c = user['is_closed']
                self.assertTrue(l)
                self.assertFalse(c)

        def test_get_users_with_foto(self):
            for user in self.get_users_with_foto():
                p = len(user['top_3_photo'])
                self.assertEqual(p, 3)





