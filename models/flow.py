# -*- coding: utf-8 -*-

import models
from orator import Model
from orator.orm import belongs_to

class Flow(Model):
    '''An representation of a process path of execution'''
    __fillable__ = ['name', 'description', 'status', 'criticality']

    @belongs_to
    def process(self):
        '''The owner of this project'''
        return models.process.Process
