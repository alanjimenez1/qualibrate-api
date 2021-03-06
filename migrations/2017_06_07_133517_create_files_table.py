from orator.migrations import Migration


class CreateFilesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('files') as table:
            table.increments('id')
            table.string('uuid')
            table.string('name')
            table.string('path')
            table.string('mime')
            table.integer('user_id')
            table.timestamps()
            table.foreign('user_id').references('id').on('users')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('files')
