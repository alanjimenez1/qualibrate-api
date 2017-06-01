# -*- coding: utf-8 -*-
"""
Entity mapping an end-user of the
application. Main associations are:
- Project
- TestAsset
"""

__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

from orator import Model
from database import db

Model.set_connection_resolver(db)
class User(Model):
    '''Person registred into Qualibrate'''
    __fillable__ = ['first_name', 'last_name', 'email']
