# -*- coding: utf-8 -*-
"""
This encloses all operations required to manipulate files
in the Qualibrate Foundation Cloud platform
"""

__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

import json
import os
import uuid
from flask import request
from flask_restplus import Namespace, Resource, fields
from werkzeug.utils import secure_filename
from .utils import UPLOADER


API = Namespace('files', description='Handling of attachments and image upload for Qualibrate')

FILE = API.model('File', {
    'name': fields.String(required=True, description='File name', example='my_file.pdf'),
    'description': fields.String(
        required=False,
        description='A brief description of the file',
        example='Snapshot of the initial screen')
})

# pylint: disable=no-self-use
@API.route('')
class FileUpload(Resource):
    """Endpoint for handling file uploads"""
    @API.expect(UPLOADER)
    def post(self):
        """
        Uploads a new file into Qualibrate

        There is a restricting policy for the types of files
        that can be uploaded in the platform.


        Allowance: [.pdf, .jpeg, .jpg, .gif, .png, .txt]
        """

        file = UPLOADER.parse_args()['file']
        UPLOAD_PATH = os.path.join(os.path.abspath('.'), 'uploads')
        file.save(os.path.join("/tmp", file.filename))

        return 'Done', 201
