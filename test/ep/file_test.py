# -*- coding: utf-8 -*-
"""
Test module for User endpoint responses
"""
__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

import unittest
from test.ep.utils import ApiRequest as http_client

class FileEndPointTest(unittest.TestCase):
    '''Files endpoint tests'''

    def test_file_upload(self):
        """
        Upload a text valid file
        """
        file_uploaded = http_client().post(":5000/files", "user_id=1 file@/sw/apps2/qualibrate-api/LICENSE")
        self.assertTrue(file_uploaded['mime'] == 'text/plain')
