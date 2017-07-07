# -*- coding: utf-8 -*-

from orator import Model
from orator.orm import belongs_to
import models

# pylint: disable=no-self-use
class Project(Model):
    '''A project is an entity that serves as a repo for assets'''
    __fillable__ = ['name', 'code', 'active']

    @belongs_to
    def user(self):
        '''The owner of this project'''
        return models.user.User
