# -*- coding: utf-8 -*-
"""
This module contains the utilities required
to manipulate responses and requests in the
API endpoints of Qualibrate
"""
__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

from flask_restplus import reqparse
import werkzeug

PAGE_OPTS = [5, 10, 20, 30, 40, 50]
PAGINATOR = reqparse.RequestParser()
PAGINATOR.add_argument('page',
                       type=int,
                       required=False,
                       default=1,
                       help='Page number',
                       location='args')
PAGINATOR.add_argument('per_page',
                       type=int,
                       required=False,
                       choices=PAGE_OPTS,
                       default=10,
                       help='Items per page',
                       location='args')

UPLOADER = reqparse.RequestParser()
UPLOADER.add_argument('file',
                     type=werkzeug.datastructures.FileStorage,
                     location='files',
                     help='File to be uploaded')
