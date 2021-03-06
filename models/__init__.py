# -*- coding: utf-8 -*-
"""
This are the entities used inside
the Qualibrate Foundation platform
together with the business logic of the
entire application
"""
__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

from database import db
from orator import Model

Model.set_connection_resolver(db)
