# -*- coding: utf-8 -*-
"""
Python-Flask based application with various endpoits
defined in Flask-restplus and swagger definitions

__http://host:5000/swagger__
"""
__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

import logging
from flask import Flask
from apis import ENDPOINT

# Enabling logging for database queries
# LOGGER = logging.getLogger('orator.connection.queries')
# LOGGER.setLevel(logging.DEBUG)
#
# # Stream log into the standard output
# LOGGER.addHandler(logging.StreamHandler())

APP = Flask(__name__)
ENDPOINT.init_app(APP)

if __name__ == '__main__':
    APP.run(debug=True, host="0.0.0.0", port=5000)
