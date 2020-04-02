from flask import request
from database.models.user import User
from database.models.heart_rate import HeartRate
from database.db import db
from flask_restplus import Resource
from datetime import datetime
from api.utility import list_to_array
from api.routes.access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utility import custom_response
from api import api
from api.custom_request import fitness_data

ns = api.namespace('heart-rates', description='Operations related to heart rates')


@ns.route('/all')
@api.doc(security='apiKey')
class HeartRatesAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        """
        Return all the heart rates
        """
        heart_rates = HeartRate.query.all()
        heart_rates = list_to_array(heart_rates)
        return custom_response(
            200,
            "All Heart Rates",
            heart_rates
        )


@ns.route('')
@api.doc(security='apiKey')
class HeartRatesApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        """
        Return all the heart rates for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        heart_rates = HeartRate.query.with_parent(current_user).all()
        heart_rates = list_to_array(heart_rates)
        return custom_response(
            200,
            "Your heart rates",
            heart_rates
        )

    @jwt_required
    @requires_access_level(2)
    @api.expect(fitness_data)
    def post(self):
        """
        Add a new heart rate for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])

        heart_rate = request.get_json()

        current_date = datetime.now()
        day_stat = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = current_date.replace(hour=23, minute=59, second=59, microsecond=59)

        old_hr = HeartRate.query.filter(User.id == current_user.id,
                                        HeartRate.timestamp >= day_stat,
                                        HeartRate.timestamp <= day_end).first()

        if old_hr is None:
            new_hr = HeartRate(
                timestamp=current_date,
                value=heart_rate['value'],
                user=current_user
            )
            new_hr.save()
            return custom_response(
                200,
                "Heart rate added",
                new_hr.id
            )

        else:
            if old_hr.value <= heart_rate['value']:
                old_hr.value = old_hr['value']
                db.session.commit()
                return custom_response(
                    200,
                    "Heart rate updated",
                    old_hr.id
                )
            else:
                return custom_response(
                    200,
                    "Heart rate already updated",
                    old_hr.id
                )


@ns.route('/<int:id>')
@api.doc(security='apiKey')
class HeartRateApi(Resource):

    @jwt_required
    @requires_access_level(1)
    @api.doc(params={'id': 'id of user'})
    def get(self, id):
        """
        Return all the heart rates for the specified user
        """
        user = User.query.filter_by(id=id).first()
        heart_rates = HeartRate.query.with_parent(user).all()
        heart_rates = list_to_array(heart_rates)
        return custom_response(
            200,
            "{} heart rates".format(user.username),
            heart_rates
        )


@ns.route('/last/<int:limit>')
@api.doc(security='apiKey')
class LastHeartRatesApi(Resource):

    @jwt_required
    @requires_access_level(2)
    @api.doc(params={'limit': 'number of element to keep'})
    def get(self, limit):
        """
        Return the last n heart rates
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])

        if current_user.is_admin() or current_user.has_child(id):
            current_user = User.find_by_username(get_jwt_identity()['username'])
            heart_rates = HeartRate.query.with_parent(current_user).limit(limit).all()
            heart_rates = list_to_array(heart_rates)
            return custom_response(
                200,
                "Last {} heart rates".format(limit),
                heart_rates
            )
        else:
            return custom_response(
                401,
                "Permission denied. User {} not a child".format(id)
            )
