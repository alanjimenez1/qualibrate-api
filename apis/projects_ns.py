# -*- coding: utf-8 -*-

import json
from flask import request
from flask_restplus import Namespace, Resource, fields
from models.project import Project as orm_project
from .utils import PAGINATOR

API = Namespace('projects', description='Project lifecycle and test asset administration')

PROJECT = API.model('Project', {
    'id': fields.String(required=False, description='Unique identifier', example='1'),
    'name': fields.String(required=True, description='Project name', example='CRM Project'),
    'code': fields.String(required=False, description='Generic identifier', example='PRJ-001'),
    'description': fields.String(
        required=False,
        description='Details about project content',
        example='Automation suite for release 101-B'),
    'active': fields.Boolean(required=False, description='In archive?', example='Y/N')
})


# pylint: disable=no-self-use
@API.route('')
class ProjectsList(Resource):
    """Endpoint for project listings results"""

    @API.marshal_list_with(PROJECT)
    @API.response(200, 'Project found')
    @API.expect(PAGINATOR)
    def get(self):
        """
        List all projects

        Returns a collection of projects paginated and consolidated
        in bundles of 10 per page
        """

        # Retrieval of pagination parameters: page, per_page
        page_args = PAGINATOR.parse_args()
        return orm_project.paginate(page_args['per_page'], page_args['page']).serialize(), 200

    @API.expect(PROJECT)
    def post(self):
        """
        Creates a new project

        It uses the code as a primarily identifier of the project
        and as credentials to authenticate in the platform.
        """

        # User skeleton
        new_project = orm_project()

        # Parsing payload from json string to dict
        new_project.set_raw_attributes(json.loads(request.data))
        if new_project.save():
            return new_project.serialize(), 201
