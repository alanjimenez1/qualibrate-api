# -*- coding: utf-8 -*-
"""
This encloses all operations required to manipulate files
in the Qualibrate Foundation Cloud platform
"""

__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

import ujson
import os
import uuid
import magic
from flask import request
from models.file import File as orm_file
from models.user import User as orm_user
from flask_restplus import Namespace, Resource, fields
from werkzeug.utils import secure_filename
from .utils import UPLOADER


API = Namespace('files', description='Handling of attachments and image upload for Qualibrate')

FILE = API.model('File', {
    'user_id': fields.Integer(required=True, description='The owner of this file', example='10'),
    'uuid': fields.String(required=False, description='Generated unique hash', example='3445-2334-2111'),
    'name': fields.String(required=True, description='File name', example='my_file.pdf'),
    'path': fields.String(required=False, description='File name', example='/device/storage/folder'),
    'mime': fields.String(required=False, description='File name', example='application/pdf')
})

# Location to store files
UPLOAD_PATH = 'uploads'

# File mime types allowed in this end point
UPLOAD_FORMAT_ALLOWANCE = ['image/png', 'application/pdf', 'image/jpeg', 'image/gif', 'text/plain']

# pylint: disable=no-self-use
@API.route('')
class FileUpload(Resource):
    """Endpoint for handling file uploads"""
    @API.expect(UPLOADER, validate=True)
    def post(self):
        """
        Uploads a new file into Qualibrate

        There is a restricting policy for the types of files
        that can be uploaded in the platform.


        Allowance: [.pdf, .jpeg, .jpg, .gif, .png, .txt]
        """
        file = UPLOADER.parse_args()['file']        

        # Allocation of request parameters to model attributes
        new_file = orm_file(API.marshal(request.data, FILE))
        new_file.uuid = str(uuid.uuid4())
        new_file.name = secure_filename(file.name)
        new_file.path = os.path.join(os.path.abspath('.'), UPLOAD_PATH, new_file.uuid)

        # # Storing file under application ./uploads
        flag = file.save(new_file.path)

        # Obtains the real mime-type of the file
        new_file.mime = magic.Magic().from_file(new_file.path)
        if not new_file.mime in UPLOAD_FORMAT_ALLOWANCE:
            API.abort(400, 'File type is not allowed')

        if orm_user.find_or_fail(request.form['user_id']).files().save(new_file):
            return new_file.serialize(), 201
