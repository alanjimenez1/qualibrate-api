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
            table.datatime('activated_at') # Email confirmed event
            table.datatime('token_at') # Account change event
            table.datatime('login_at') # Last login event
            table.datatime('logou_at') # Last logout event
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
