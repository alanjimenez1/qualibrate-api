# -*- coding: utf-8 -*-
"""
Test module for User endpoint responses
"""
__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

import unittest
from test.ep.utils import ApiRequest as http_client

class UserEndPointTest(unittest.TestCase):
    '''User endpoint tests'''

    def test_user_list(self):
        """
        Confirm that endpoint complies with structure
        """
        user_list = http_client().get(":5000/users")
        self.assertTrue(len(user_list) > 0)

    def test_user_pagination(self):
        """
        Confirm that endpoint paginates
        """
        user_list = http_client().get(":5000/users?per_page=20")
        self.assertTrue(len(user_list) == 20)
