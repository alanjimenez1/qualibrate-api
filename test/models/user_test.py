import unittest
from models.user import User

class UserModelTest(unittest.TestCase):

    def test_attributes(self):
        """
        Confirm all the expected attributes of the model
        """
        user = User.first()
        expected_attrs = set(["id","email","last_name","first_name"])
        actual_attrs = set(User.first().get_attributes().keys())
        self.assertTrue(expected_attrs.issubset(actual_attrs))

    def test_pagination(self):
        """
        Retrieves pages of users from the database
        """
        user_list = User.paginate(10,1)
        self.assertEqual(len(user_list),10)
