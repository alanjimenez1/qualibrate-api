# -*- coding: utf-8 -*-
"""
This encloses all operations required to manipulate users
in the Qualibrate Foundation Cloud platform
"""

__author__ = "@canimus"
__license__ = "MIT"
__revision__ = "1.0"

import ujson
from flask import request
from flask_restplus import Namespace, Resource, fields
from models.user import User as orm_user
from models.project import Project as orm_project
from models.file import File as orm_file
from orator.exceptions.orm import ModelNotFound
from orator.exceptions.query import QueryException
from .utils import PAGINATOR

API = Namespace('users', description='Platform access administration')

USER = API.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name',
        example='John',
        pattern=r'^[a-zA-Z]'),
    'last_name': fields.String(
        required=True,
        description='Last name',
        example='Smith',
        pattern="^[a-zA-Z]"),
    'email': fields.String(
        required=True,
        description='Contact email',
        example='jsmith@gmail.com',
        pattern=r"[^@]+@[^@]+\.[^@]+")
})

USER_DATA = USER.inherit('User', USER, {
    'id': fields.Integer(required=False, description='Unique identifier', example='1')
})


# pylint: disable=no-self-use
# pylint: disable=maybe-no-member
@API.route('')
class UsersList(Resource):
    """Endpoint for list-based user results."""

    @API.marshal_list_with(USER_DATA)
    @API.response(200, 'Users list')
    @API.expect(PAGINATOR)
    def get(self):
        """
        List all users

        Returns a collection of users paginated and consolidated
        in bundles of 10 per page
        """

        # Retrieval of pagination parameters: page, per_page
        page_args = PAGINATOR.parse_args()
        return orm_user.for_page(page_args['page'], page_args['per_page']).get().serialize(), 200


    @API.expect(USER, validate=True)
    def post(self):
        """
        Creates a new user

        It uses the email as a primarily identifier of the user
        and as credentials to authenticate in the platform.
        """
        try:
            new_user = orm_user(API.marshal(ujson.loads(request.data), USER))
            flag = new_user.save()
        except QueryException:
            API.abort(code=400, message='Integrity violation')

        if flag:
            return new_user.serialize(), 201

@API.route('/<int:user_id>')
class User(Resource):
    """Endpoint for users operations."""

    @API.response(200, 'User found', USER_DATA)
    @API.marshal_with(USER_DATA)
    def get(self, user_id):
        """
        Fetch a user by its identifier

        Users are identified by a unique number
        as an immutable integer that identifies them.
        """

        try:
            return orm_user.find_or_fail(user_id).serialize()
        except ModelNotFound:
            API.abort(code=404, message='User not found')


    @API.response(204, 'User successfully deleted')
    def delete(self, user_id):
        """
        Deletes an existing user

        Removes in cascade all information associated
        to an individual user in Qualibrate
        """
        try:
            old_user = orm_user.find_or_fail(user_id)
            flag = old_user.delete()
        except ModelNotFound:
            API.abort(code=404, message='User not found')
        except QueryException:
            API.abort(code=400, message='Integrity violation')

        if flag:
            return user_id, 204


    @API.response(202, 'User successfully updated')
    @API.expect(USER)
    def put(self, user_id):
        """
        Updates an existing user

        The body of the requests contains a json representation
        of the User model with the new set of attributes
        """

        # Empty user creation
        current_user = orm_user.find_or_fail(user_id)
        current_user.set_raw_attributes(ujson.loads(request.data))
        if current_user.save():
            return current_user.serialize(), 202

@API.route('/<int:user_id>/projects')
class UserProjects(Resource):
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
            return orm_user.find_or_fail(user_id).projects.serialize()
        except ModelNotFound:
            API.abort(404)

@API.route('/<int:user_id>/projects/<int:project_id>')
class UserAddSProjects(Resource):
    """
    Assigns the project ownership to a singular user

    Users can own many projects, this association provides
    a specified user the ownership of a project
    """
    def put(self, user_id, project_id):
        """
        User takes ownership of a project
        """
        operation = orm_project.find(project_id).user().associate(orm_user.find(user_id))
        if operation.save():
            return orm_user.with_('projects').get().filter(
                lambda x: x.id == user_id
                ).serialize(), 201

@API.route('/<int:user_id>/files')
class UserFiles(Resource):
    """
    Fetch all the files for an individual user

    Retrieve all reference files that belong
    to this user, it includes attachments, images,
    references and all the files used in Qualibrate
    """
    def get(self, user_id):
        """
        A list of files that belong to a particular user
        """
        try:            
            return orm_file.select('uuid','name','mime','created_at','updated_at').where('user_id','=',user_id).get().serialize(), 200
        except ModelNotFound:
            API.abort(404)
