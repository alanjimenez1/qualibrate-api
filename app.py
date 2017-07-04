# -*- coding: utf-8 -*-

import logging
from flask import Flask
from apis import ENDPOINT

# Log SQL Queries
LOGGER = logging.getLogger('orator.connection.queries')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(logging.StreamHandler())

APP = Flask(__name__)
ENDPOINT.init_app(APP)

if __name__ == '__main__':
    APP.run(debug=True, host="0.0.0.0", port=5000)
