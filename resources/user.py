from flask import Response, request
from database.models.user import User
from database.models.user import USER_ROLE
from flask_restful import Resource
from .utility import list_to_json
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from .access_restrictions import requires_access_level


class UsersAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        users = User.query.all()
        users = list_to_json(users)
        return Response(users, mimetype="application/json", status=200)


class UsersApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        current_user = get_jwt_identity()
        user = User.find_by_username(current_user['username'])
        return user.to_dict(), 200

    def post(self):
        body = request.get_json()

        if User.find_by_username(body['username']):
            return {'message': 'User {} already exists'.format(body['username'])}, 401

        user = User(
            username=body['username'],
            password=User.generate_hash(body['password']),
            role=USER_ROLE['user']
        )
        try:
            user.save()
            access_token = create_access_token(identity=create_identity(user))
            refresh_token = create_refresh_token(identity=create_identity(user))
            return {
                'message': 'User {} was created'.format(user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                   }, 200
        except:
            return {'message': 'Something went wrong'}, 500


class UserApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return user.to_dict(), 200


def create_identity(user):
    user_identity = {
        'username': user.username,
        'role': user.role
    }
    return user_identity
