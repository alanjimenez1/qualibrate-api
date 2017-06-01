from orator.migrations import Migration


class CreateProjectsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('projects') as table:
            table.string('id')
            table.string('name')
            table.string('code')
            table.boolean('active')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('projects')
