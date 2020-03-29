from flask import request
from database.models.user import User
from database.models.calorie import Calorie
from flask_restplus import Resource
from datetime import datetime
from api.utility import list_to_array
from api.routes.access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utility import custom_response
from api import api
from api.custom_request import fitness_data

ns = api.namespace('calories', description='Operation related to category')


@ns.route('/all')
@api.doc(security='apiKey')
class CaloriesAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        """
        Return all the calories
        """
        calories = Calorie.query.all()
        calories = list_to_array(calories)
        return custom_response(
            200,
            "All calories",
            calories
        )


@ns.route('')
@api.doc(security='apiKey')
class CaloriesApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        """
        Return all the calories for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        calories = Calorie.query.with_parent(current_user).all()
        calories = list_to_array(calories)
        return custom_response(
            200,
            "Your calories",
            calories
        )

    @jwt_required
    @requires_access_level(2)
    @api.expect(fitness_data)
    def post(self):
        """
        Add a new calorie for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        calorie = request.get_json()
        new_calories = Calorie(
            timestamp=datetime.now(),
            value=calorie['value'],
            user=current_user
        )
        new_calories.save()
        return custom_response(
            200,
            "Calorie added",
            new_calories.id
        )


@ns.route('/<int:id>')
@api.doc(security='apiKey')
class CalorieApi(Resource):

    @jwt_required
    @requires_access_level(1)
    @api.doc(params={'id': 'id of the user'})
    def get(self, id):
        """
        Return all the calories for the specified user
        """
        user = User.query.filter_by(id=id).first()
        calories = Calorie.query.with_parent(user).all()
        calories = list_to_array(calories)
        return custom_response(
            200,
            "{} calories".format(user.username),
            calories
        )

