 # -*- coding: utf-8 -*-
from flask import request
from flask_restplus import Namespace, Resource, fields
from .utils import pagination
from database import db
from models.user import User as orm_user
from schema import Schema
import json

api = Namespace('users', description='Platform access administration')

user = api.model('User', {
    'id': fields.Integer(required=True, description='Unique identifier', example='1'),
    'first_name': fields.String(required=True, description='First name', example='John'),
    'last_name': fields.String(required=True, description='Last name', example='Smith'),
    'email': fields.String(required=True, description='Contact email', example='jsmith@gmail.com')
})

@api.route('')
class UsersList(Resource):

    @api.marshal_list_with(user)
    @api.response(200, 'User found')
    @api.expect(pagination)
    def get(self):
        """
        List all users

        Returns a collection of users paginated and consolidated
        in bundles of 10 per page
        """
        return orm_user.all().serialize(), 200

    @api.expect(user)
    def post(self):
        """
        Creates a new user

        It uses the email as a primarily identifier of the user
        and as credentials to authenticate in the platform.
        """

        # Empty user creation
        new_user = orm_user()

        # Parsing payload from json string to dict
        new_user.set_raw_attributes(json.loads(request.data))
        if new_user.save():
            return new_user.serialize(), 201
        else:
            None, 422


@api.route('/<int:id>')
@api.response(404, 'User not found')
class User(Resource):
    @api.marshal_with(user)
    @api.response(200, 'User found')
    def get(self, id):
        """
        Fetch a user by its identifier

        Users are identified by a unique number
        as an immutable integer that identifies them.
        """

        try:
            return orm_user.find(id).serialize() or api.abort(404)
        except Exception as e:
            api.abort(404)

    @api.response(204, 'User successfully deleted')
    def delete(self, id):
        """
        Deletes an existing user

        Removes in cascade all information associated
        to an individual user in Qualibrate
        """

        old_user = orm_user.find(id)

        if old_user.delete():
            return id, 204
        else:
            return False, 422

    @api.response(202, 'User successfully updated')
    @api.expect(user)
    def put(self, id):
        """
        Updates an existing user

        The body of the requests contains a json representation
        of the User model with the new set of attributes
        """

        # Empty user creation
        current_user = orm_user.find(id)

        # Parsing payload from json string to dict
        current_user.set_raw_attributes(json.loads(request.data))
        if current_user.save():
            return current_user.serialize(), 202
        else:
            None, 422
