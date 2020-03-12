from flask import Response, request
from database.db import db
from database.models.user import User
from database.models.meter import Meter
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_json


class MetersApi(Resource):
    def get(self):
        meters = Meter.query.all()
        meters = list_to_json(meters)
        return Response(meters, mimetype="application/json", status=200)


class MeterApi(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        meters = Meter.query.with_parent(user).all()
        meters = list_to_json(meters)
        return Response(meters, mimetype="application/json", status=200)

    def post(self, id):
        user = User.query.filter_by(id=id).first()
        meter = request.get_json()
        new_meter = Meter(
            timestamp=datetime.now(),
            value=meter['value'],
            user=user
        )
        db.session.add(new_meter)
        db.session.commit()
        return {'id': str(new_meter.id)}, 200
