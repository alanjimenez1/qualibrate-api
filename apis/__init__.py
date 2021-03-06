# -*- coding: utf-8 -*-

from flask_restplus import Api
from .users_ns import API as users
from .projects_ns import API as projects
from .files_ns import API as files

ENDPOINT = Api(
    title='Qualibrate Foundation API',
    version='1.0',
    description='Testing, documentation and training seamless framework'
)

ENDPOINT.add_namespace(users)  # Users
ENDPOINT.add_namespace(projects)  # Projects
ENDPOINT.add_namespace(files)  # Files
