from flask import request
from database.models.user import User
from database.models.meter import Meter
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_array
from .access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utility import custom_response


class MetersAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        meters = Meter.query.all()
        meters = list_to_array(meters)
        return custom_response(
            200,
            "All meters",
            meters
        )


class MetersApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])
        meters = Meter.query.with_parent(current_user).all()
        meters = list_to_array(meters)
        return custom_response(
            200,
            "Your meters",
            meters
        )

    @jwt_required
    @requires_access_level(2)
    def post(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])
        meter = request.get_json()
        new_meter = Meter(
            timestamp=datetime.now(),
            value=meter['value'],
            user=current_user
        )
        new_meter.save()
        return custom_response(
            200,
            "Mater added",
            meter.id
        )


class MeterApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        meters = Meter.query.with_parent(user).all()
        meters = list_to_array(meters)
        return custom_response(
            200,
            "{} meters".format(user.username),
            meters
        )

