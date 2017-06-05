# -*- coding: utf-8 -*-
"""
This encloses all operations required to manipulate users
in the Qualibrate Foundation Cloud platform
"""

__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

import json
import uuid
from flask import request
from flask_restplus import Namespace, Resource, fields
from models.user import User as orm_user
from orator.exceptions.orm import ModelNotFound
from .utils import PAGINATOR

API = Namespace('users', description='Platform access administration')

USER = API.model('User', {
    'id': fields.Integer(required=True, description='Unique identifier', example='1'),
    'first_name': fields.String(required=True, description='First name', example='John'),
    'last_name': fields.String(required=True, description='Last name', example='Smith'),
    'email': fields.String(required=True, description='Contact email', example='jsmith@gmail.com')
})

# pylint: disable=no-self-use
@API.route('')
class UsersList(Resource):
    """Endpoint for list-based user results."""

    @API.marshal_list_with(USER)
    @API.response(200, 'User found')
    @API.expect(PAGINATOR)
    def get(self):
        """
        List all users

        Returns a collection of users paginated and consolidated
        in bundles of 10 per page
        """

        # Retrieval of pagination parameters: page, per_page
        page_args = PAGINATOR.parse_args()
        return orm_user.paginate(page_args['per_page'], page_args['page']).serialize(), 200

    @API.expect(USER)
    def post(self):
        """
        Creates a new user

        It uses the email as a primarily identifier of the user
        and as credentials to authenticate in the platform.
        """

        # User skeleton
        new_user = orm_user()
        new_user.id = uuid.uuid1().hex

        # Parsing payload from json string to dict
        new_user.set_raw_attributes(json.loads(request.data))
        if new_user.save():
            return new_user.serialize(), 201


@API.route('/<int:id>')
@API.response(404, 'User not found')
class User(Resource):
    """Endpoint for users operations."""

    @API.marshal_with(USER)
    @API.response(200, 'User found')
    def get(self, user_id):
        """
        Fetch a user by its identifier

        Users are identified by a unique number
        as an immutable integer that identifies them.
        """

        try:
            return orm_user.find_or_fail(user_id).serialize() or API.abort(404)
        except ModelNotFound:
            API.abort(404)

    @API.response(204, 'User successfully deleted')
    def delete(self, user_id):
        """
        Deletes an existing user

        Removes in cascade all information associated
        to an individual user in Qualibrate
        """

        old_user = orm_user.find(user_id)

        if old_user.delete():
            return id, 204


    @API.response(202, 'User successfully updated')
    @API.expect(USER)
    def put(self, user_id):
        """
        Updates an existing user

        The body of the requests contains a json representation
        of the User model with the new set of attributes
        """

        # Empty user creation
        current_user = orm_user.find(user_id)

        # Parsing payload from json string to dict
        current_user.set_raw_attributes(json.loads(request.data))
        if current_user.save():
            return current_user.serialize(), 202

@API.route('/<int:id>/projects')
@API.response(404, 'User without projects')
class UserWithProjects(Resource):
    """
    Fetch all the projects for an individual user

    Projects are the test asset containers in Qualibrate
    and contains all information about a test project
    """
    def get(self, user_id):
        """
        A list of projects that belong to a particular user
        """
        try:
            return orm_user.find_or_fail(user_id).projects.serialize() or API.abort(404)
        except ModelNotFound:
            API.abort(404)
