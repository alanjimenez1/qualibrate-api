from orator.migrations import Migration


class CreateProjectsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('projects') as table:
            table.increments('id')
            table.string('name')
            table.long_text('description').nullable()
            table.string('code').nullable()
            table.string('icon').nullable()
            table.boolean('active').default(False)
            table.integer('user_id')
            table.timestamps()
            table.foreign('user_id').references('id').on('users')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('projects')
