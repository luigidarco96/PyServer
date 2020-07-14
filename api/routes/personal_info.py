from flask import request
from database.models.user import User
from database.models.personal_info import PersonalInfo
from flask_restplus import Resource
from api.utility import list_to_array
from api.routes.access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utility import custom_response
from api import api
from api.custom_request import personal_info_data

ns = api.namespace('personal-info', description='Operation related to user\'s personal info')


@ns.route('/all')
@api.doc(security='apiKey')
class PersonalInfoAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        """
        Return all the users' personal info
        """
        personal_info = PersonalInfo.query.all()
        personal_info = list_to_array(personal_info)
        return custom_response(
            200,
            "All personal info",
            personal_info
        )


@ns.route('')
@api.doc(security='apiKey')
class PersonalInfoApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        """
        Return all the personal info for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        personal_info = PersonalInfo.query.with_parent(current_user).order_by(PersonalInfo.timestamp.desc()).all()
        personal_info = list_to_array(personal_info)
        return custom_response(
            200,
            "Your personal info",
            personal_info
        )

    @jwt_required
    @requires_access_level(2)
    @api.expect(personal_info_data)
    def post(self):
        """
        Add a new personal info for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])

        personal_info = request.get_json()

        new_personal_info = PersonalInfo(
            weight=personal_info['weight'],
            height=personal_info['height'],
            user=current_user
        )

        new_personal_info.save()

        return custom_response(
            200,
            "Personal Info added",
            new_personal_info.id
        )


