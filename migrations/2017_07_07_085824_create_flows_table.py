from orator.migrations import Migration


class CreateFlowsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('flows') as table:
            table.increments('id')  # int
            table.string('name')
            table.string('criticality').nullable()
            table.enum('status', ['designed', 'tested', 'trained', 'released'])
            table.string('description').nullable() #  Brief description of flow
            table.integer('type')
            table.timestamps()
            table.index('id')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('flows')
