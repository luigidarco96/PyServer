from flask import Response, request
from database.models.user import User
from database.models.heart_rate import HeartRate
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_json
from .access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity


class HeartRatesAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        heart_rates = HeartRate.query.all()
        heart_rates = list_to_json(heart_rates)
        return Response(heart_rates, mimetype="application/json", status=200)


class HeartRatesApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])
        heart_rates = HeartRate.query.with_parent(current_user).all()
        heart_rates = list_to_json(heart_rates)
        return Response(heart_rates, mimetype="application/json", status=200)

    @jwt_required
    @requires_access_level(2)
    def post(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])
        heart_rate = request.get_json()
        new_heart_rate = HeartRate(
            timestamp=datetime.now(),
            value=heart_rate['value'],
            user=current_user
        )
        new_heart_rate.save()
        return {'id': str(new_heart_rate.id)}, 200


class HeartRateApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        heart_rates = HeartRate.query.with_parent(user).all()
        heart_rates = list_to_json(heart_rates)
        return Response(heart_rates, mimetype="application/json", status=200)

