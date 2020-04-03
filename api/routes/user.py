from flask import request
from database.models.user import User
from database.models.user import USER_ROLE
from flask_restplus import Resource
from api.utility import list_to_array
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from api.routes.access_restrictions import requires_access_level
from api.utility import custom_response
from api import api
from api.custom_request import login_data

ns = api.namespace('users', description='Operations related to users')


@ns.route('/all')
@api.doc(security='apiKey')
class UsersAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        """
        Return all the users
        """
        users = User.query.all()
        users = list_to_array(users)
        return custom_response(
            200,
            "All users",
            users
        )


@ns.route('/children')
@api.doc(security='apiKey')
class UsersChildrenApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self):
        """
        Return all the children for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        children = current_user.family_members.all()
        children = list_to_array(children)
        return custom_response(
            200,
            "{}'s children".format(current_user.username),
            children
        )


@ns.route('')
class UsersApi(Resource):

    @jwt_required
    @requires_access_level(2)
    @api.doc(security='apiKey')
    def get(self):
        """
        Return the information for the caller user
        """
        user = User.find_by_username(get_jwt_identity()['username'])
        return custom_response(
            200,
            "User {}".format(user.username),
            user.to_dict()
        )

    @api.expect(login_data)
    def post(self):
        """
        Add a new user
        """
        body = request.get_json()

        if User.find_by_username(body['username']):
            return custom_response(
                401,
                'User {} already exists'.format(body['username'])
            )

        user = User(
            username=body['username'],
            password=User.generate_hash(body['password']),
            role=USER_ROLE['user']
        )
        try:
            user.save()
            access_token = create_access_token(identity=create_identity(user))
            refresh_token = create_refresh_token(identity=create_identity(user))
            return custom_response(
                200,
                'User {} was created'.format(user.username),
                {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            )
        except:
            return custom_response(
                500,
                'Something went wrong'
            )


@ns.route('/<int:id>')
@api.doc(security='apiKey')
@api.doc(params={'id': 'id of user'})
class UserApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self, id):
        """
        Return the information of the specified user
        """
        user = User.query.filter_by(id=id).first()
        if user is None:
            return custom_response(
                404,
                "User {} not found".format(id)
            )
        return custom_response(
            200,
            "User {}".format(user.username),
            user.to_dict()
        )

    @jwt_required
    @requires_access_level(0)
    @api.doc(security='apiKey')
    @api.expect(login_data)
    def put(self):
        """
        Update information for the specified user
        """
        user = User.find_by_username(get_jwt_identity()['username'])
        new_user = request.get_json()
        user.username = new_user['username']
        user.password = User.generate_hash(new_user['password'])
        user.update()
        return custom_response(
            200,
            "Your information was updated",
            user.to_dict()
        )

    @jwt_required
    @requires_access_level(0)
    def delete(self, id):
        """
        Delete the specified user
        """
        user = User.query.filter_by(id=id).first()
        if user is None:
            return custom_response(
                404,
                "User {} not found".format(id)
            )
        user.delete()
        return custom_response(
            200,
            "User {} deleted".format(id)
        )


def create_identity(user):
    user_identity = {
        'username': user.username,
        'role': user.role
    }
    return user_identity
