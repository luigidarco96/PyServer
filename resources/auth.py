from flask import request
from flask_restful import Resource
from database.models.user import User
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from database.models.revoked_token import RevokedToken
from .utility import custom_response


class LoginApi(Resource):

    def post(self):
        body = request.get_json()
        user = User.find_by_username(body['username'])
        if not user:
            return custom_response(401, 'User {} doesn\'t exist'.format(body['username']))

        if User.verify_hash(body['password'], user.password):
            access_token = create_access_token(create_identity(user), expires_delta=False)
            refresh_token = create_refresh_token(create_identity(user))
            return custom_response(
                200,
                'Logged in as {}'.format(user.username),
                {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            )
        else:
            return custom_response(
                401,
                'Username or password wrong'
            )


class LogoutAccess(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            return custom_response(
                200,
                'Access token has been revoked'
            )
        except:
            return custom_response(
                500,
                'Something went wrong'
            )


class LogoutRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            return custom_response(
                200,
                'Refresh token has been revoked'
            )
        except:
            return custom_response(
                500,
                'Something went wrong'
            )


class RefreshToken(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return custom_response(
            200,
            'Access token refreshed',
            access_token
        )


def create_identity(user):
    user_identity = {
        'username': user.username,
        'role': user.role
    }
    return user_identity
