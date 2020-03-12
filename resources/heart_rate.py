from flask import Response, request
from database.db import db
from database.models.user import User
from database.models.heart_rate import HeartRate
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_json


class HeartRatesApi(Resource):
    def get(self):
        heart_rates = HeartRate.query.all()
        heart_rates = list_to_json(heart_rates)
        return Response(heart_rates, mimetype="application/json", status=200)


class HeartRateApi(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        heart_rates = HeartRate.query.with_parent(user).all()
        heart_rates = list_to_json(heart_rates)
        return Response(heart_rates, mimetype="application/json", status=200)

    def post(self, id):
        user = User.query.filter_by(id=id).first()
        heart_rate = request.get_json()
        new_heart_rate = HeartRate(
            timestamp=datetime.now(),
            value=heart_rate['value'],
            user=user
        )
        db.session.add(new_heart_rate)
        db.session.commit()
        return {'id': str(new_heart_rate.id)}, 200
