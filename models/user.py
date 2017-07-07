# -*- coding: utf-8 -*-

import models
from orator import Model
from orator.orm import has_many

# pylint: disable=no-self-use
class User(Model):
    '''Person registred into Qualibrate'''
    __fillable__ = ['first_name', 'last_name', 'email']
    __dates__ = ['activated_at', 'token_at', 'login_at']

    @has_many
    def projects(self):
        '''A list of projects owned by this user'''
        return models.project.Project

    @has_many
    def files(self):
        '''A list of files owned by this user'''
        return models.file.File
