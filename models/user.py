from orator import Model
from database import db

Model.set_connection_resolver(db)
class User(Model):
    __fillable__ = ['first_name', 'last_name', 'email']
