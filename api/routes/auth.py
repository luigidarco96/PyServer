from flask import request
from flask_restplus import Resource
from database.models.user import User
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from database.models.revoked_token import RevokedToken
from api.utility import custom_response
from api import api
from api.custom_request import login_data

ns = api.namespace('', description='Operations related to authentication')


@ns.route('/sign-in')
@api.expect(login_data)
class LoginApi(Resource):

    def post(self):
        """
        Create new user session
        """
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


@ns.route('/sign-out/access')
@api.doc(security='apiKey')
class LogoutAccess(Resource):

    @jwt_required
    def post(self):
        """
        Revoke user access token
        """
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


@ns.route('/sign-out/refresh')
@api.doc(security='apiKey')
class LogoutRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        """
        Revoke user refresh token
        """
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


@ns.route('/refresh-token')
class RefreshToken(Resource):

    @jwt_refresh_token_required
    def post(self):
        """
        Refresh token
        """
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
