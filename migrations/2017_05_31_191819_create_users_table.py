from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.increments('id')  # int
            table.string('uid').nullable()  # OAuth
            table.string('provider').nullable()  # OAuth
            table.string('first_name')
            table.string('last_name')
            table.string('email').unique()
            table.boolean('active').default(False)
            table.datetime('activated_at').nullable()  # Email confirmed event
            table.datetime('token_at').nullable()  # Account change event
            table.datetime('login_at').nullable()  # Last login event
            table.datetime('logout_at').nullable()  # Last logout event
            table.timestamps()
            table.index('id')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
