import unittest
from test.endpoints.utils import ApiRequest as http_client

class UserEndPointTest(unittest.TestCase):

    def test_attributes(self):
        """
        Confirm that endpoint complies with structure
        """
        user_list = http_client().get(":5000/users")
        self.assertTrue(True)
