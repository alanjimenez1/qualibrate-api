# -*- coding: utf-8 -*-
"""
Entity for storing file
attachments in the platform
"""

__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

from orator import Model
from orator.orm import belongs_to
import models

class File(Model):
    '''A file is the persistent reference of an attachment'''
    __fillable__ = ['uuid', 'name', 'path', 'mime']

    @belongs_to
    def user(self):
        '''The owner of this file'''
        return models.user.User
