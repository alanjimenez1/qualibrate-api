# -*- coding: utf-8 -*-
"""
This module contains the utilities required
to perform testing verifications in EndPoints
including a custom HTTP Client
"""

__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

import ujson
import subprocess

# pylint: disable=no-self-use
class ApiRequest:
    '''A custom HTTP Client'''
    def get(self, url):
        '''Performs a HTTP GET method and returns a JSON object'''
        return ujson.loads(subprocess.getoutput("http GET %s" % url))

    def post(self, url, data):
        '''Performs a HTTP POST method and returns a JSON object'''
        return ujson.loads(subprocess.getoutput("http POST %s %s" % (url, data)))
