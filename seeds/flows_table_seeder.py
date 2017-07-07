import uuid
from orator.seeds import Seeder
from orator.orm import Factory
from models.flow import Flow

class FlowsTableSeeder(Seeder):

    def flows_factory(self, faker):
        """
        Defines the template of user test records
        """
        return {
            'name' : faker.company(),
            'criticality' : 5,
            'status': 'designed',
            'description': faker.name(),
            'type' : 1            
        }

    def run(self):
        """
        Run the database seeds.
        """
        self.factory.register(Flow, self.flows_factory)

        # Adding 50 users
        self.factory(Flow, 10).create()
