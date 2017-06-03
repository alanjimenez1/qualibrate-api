from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.string('id')  # Unique UUID
            table.string('uid') # OAuth
            table.string('provider') # OAuth
            table.string('first_name')
            table.string('last_name')
            table.string('email')
            table.boolean('active')
            table.datetime('activated_at').nullable() # Email confirmed event
            table.datetime('token_at').nullable() # Account change event
            table.datetime('login_at').nullable() # Last login event
            table.datetime('logou_at').nullable() # Last logout event
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
