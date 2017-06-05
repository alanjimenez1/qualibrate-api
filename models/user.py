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
from orator.orm import has_many
import models

# pylint: disable=no-self-use
class User(Model):
    '''Person registred into Qualibrate'''
    __fillable__ = ['first_name', 'last_name', 'email']
    __dates__ = ['activated_at', 'token_at', 'login_at']

    @has_many
    def projects(self):
        '''A list of projects owned by this user'''
        return models.project.Project
