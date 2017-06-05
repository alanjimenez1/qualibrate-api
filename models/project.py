# -*- coding: utf-8 -*-
"""
Entity mapping an projects
hosted in the application.
- User
- TestAsset
"""

__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

from orator import Model
from database import db
from orator import Model
from orator.orm import belongs_to

class Project(Model):
    '''A project is an entity that serves as a repo for assets'''
    __fillable__ = ['name', 'code', 'active']

    @belongs_to
    def user(self):
        return User
