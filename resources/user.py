from flask import request
from database.models.user import User
from database.models.user import USER_ROLE
from flask_restful import Resource
from .utility import list_to_array
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from .access_restrictions import requires_access_level
from .utility import custom_response


class UsersAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        users = User.query.all()
        users = list_to_array(users)
        return custom_response(
            200,
            "All users",
            users
        )


class UsersApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        current_user = get_jwt_identity()
        user = User.find_by_username(current_user['username'])
        return custom_response(
            200,
            "User {}".format(user.username),
            user.to_dict()
        )

    def post(self):
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


class UserApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self, id):
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


def create_identity(user):
    user_identity = {
        'username': user.username,
        'role': user.role
    }
    return user_identity
