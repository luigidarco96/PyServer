from flask import request
from database.models.user import User
from database.models.calorie import Calorie
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_array
from .access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utility import custom_response


class CaloriesAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        calories = Calorie.query.all()
        calories = list_to_array(calories)
        return custom_response(
            200,
            "All calories",
            calories
        )


class CaloriesApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
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
    def post(self):
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


class CalorieApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        calories = Calorie.query.with_parent(user).all()
        calories = list_to_array(calories)
        return custom_response(
            200,
            "{} calories".format(user.username),
            calories
        )

