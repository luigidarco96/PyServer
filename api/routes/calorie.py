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

        current_date = datetime.now()
        day_stat = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = current_date.replace(hour=23, minute=59, second=59, microsecond=59)

        old_calorie = Calorie.query.filter(User.id == current_user.id,
                                           Calorie.timestamp >= day_stat,
                                           Calorie.timestamp <= day_end).first()

        if old_calorie is None:
            new_calorie = Calorie(
                timestamp=current_date,
                value=calorie['value'],
                user=current_user
            )
            new_calorie.save()
            return custom_response(
                200,
                "Calorie added",
                new_calorie.id
            )

        else:
            if old_calorie.value <= calorie['value']:
                old_calorie.value = calorie['value']
                old_calorie.update()
                return custom_response(
                    200,
                    "Calorie updated",
                    old_calorie.id
                )
            else:
                return custom_response(
                    200,
                    "Calorie already updated",
                    old_calorie.id
                )


@ns.route('/user/<int:id>')
@api.doc(security='apiKey', params={'id': 'id of the user'})
class CalorieApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self, id):
        """
        Return all the calories for the specified user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])

        if current_user.is_admin() or current_user.has_child(id):
            user = User.query.filter_by(id=id).first()
            calories = Calorie.query.with_parent(user).all()
            calories = list_to_array(calories)
            return custom_response(
                200,
                "{} calories".format(user.username),
                calories
            )
        else:
            return custom_response(
                401,
                "Permission denied. User {} not a child".format(id)
            )
