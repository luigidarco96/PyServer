from flask import Response, request
from database.models.user import User
from database.models.meter import Meter
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_json
from .access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity


class MetersAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        meters = Meter.query.all()
        meters = list_to_json(meters)
        return Response(meters, mimetype="application/json", status=200)


class MetersApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])
        meters = Meter.query.with_parent(current_user).all()
        meters = list_to_json(meters)
        return Response(meters, mimetype="application/json", status=200)

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
        return {'id': str(new_meter.id)}, 200


class MeterApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        meters = Meter.query.with_parent(user).all()
        meters = list_to_json(meters)
        return Response(meters, mimetype="application/json", status=200)

