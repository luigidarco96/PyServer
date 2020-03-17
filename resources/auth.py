from flask import Response, request
from flask_restful import Resource
from database.models.user import User
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from database.models.revoked_token import RevokedToken


class LoginApi(Resource):

    def post(self):
        body = request.get_json()
        user = User.find_by_username(body['username'])
        if not user:
            return {'message': 'User {} doesn\'t exist'.format(body['username'])}, 401

        if User.verify_hash(body['password'], user.password):
            access_token = create_access_token(create_identity(user))
            refresh_token = create_refresh_token(create_identity(user))
            return {
                       'message': 'Logged in as {}'.format(user.username),
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        else:
            return {'message': 'Wrong credentials'}, 401


class LogoutAccess(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class LogoutRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class RefreshToken(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


def create_identity(user):
    user_identity = {
        'username': user.username,
        'role': user.role
    }
    return user_identity
