from random import randint
from orator.seeds import Seeder
from models.project import Project

class ProjectTableSeeder(Seeder):

    def projects_factory(self, faker):
        """
        Defines the template of user test records
        """
        return {
            'name' : faker.company(),
            'description' : faker.paragraph(),
            'code': faker.isbn10(separator="-"),
            'active' : True,
            'user_id' : randint(1,50)
        }

    def run(self):
        """
        Run the database seeds.
        """
        self.factory.register(Project, self.projects_factory)

        # Adding 50 projects
        self.factory(Project, 50).create()
