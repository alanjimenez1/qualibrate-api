from orator.seeds import Seeder
from orator.orm import Factory
from models.user import User
import uuid

class UserTableSeeder(Seeder):

    def users_factory(self, faker):
        """
        Defines the template of user test records
        """
        return {
            'id' : uuid.uuid1().hex,
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'email' : faker.email()
        }

    def run(self):
        """
        Run the database seeds.
        """
        self.factory.register(User, self.users_factory)

        # Adding 50 users
        self.factory(User, 50).create()
