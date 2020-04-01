from flask import request
from database.models.user import User
from database.models.meter import Meter
from database.db import db
from flask_restplus import Resource
from datetime import datetime
from api.utility import list_to_array
from api.routes.access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utility import custom_response
from api import api
from api.custom_request import fitness_data

ns = api.namespace('meters', description='Operations related to meters')


@ns.route('/all')
@api.doc(security='apiKey')
class MetersAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        """
        Return all the meters
        """
        meters = Meter.query.all()
        meters = list_to_array(meters)
        return custom_response(
            200,
            "All meters",
            meters
        )


@ns.route('')
@api.doc(security='apiKey')
class MetersApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        """
        Return all the meters for the caller user
        """
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
    @api.expect(fitness_data)
    def post(self):
        """
        Add a new meter for the caller caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])

        meter = request.get_json()

        current_date = datetime.now()
        day_stat = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = current_date.replace(hour=23, minute=59, second=59, microsecond=59)

        old_meter = Meter.query.filter(User.id == current_user.id,
                                       Meter.timestamp >= day_stat,
                                       Meter.timestamp <= day_end).first()

        if old_meter is None:
            new_meter = Meter(
                timestamp=current_date,
                value=meter['value'],
                user=current_user
            )
            new_meter.save()
            return custom_response(
                200,
                "Meter added",
                new_meter.id
            )
        else:
            if old_meter.value <= meter['value']:
                old_meter.value = meter['value']
                db.session.commit()
                return custom_response(
                    200,
                    "Meter updated",
                    old_meter.id
                )
            else:
                return custom_response(
                    200,
                    "Meter already updated",
                    old_meter.id
                )


@ns.route('/<int:id>')
@api.doc(security='apiKey')
class MeterApi(Resource):

    @jwt_required
    @requires_access_level(1)
    @api.doc(params={'id': 'id of user'})
    def get(self, id):
        """
        Return all the meters for the specified user
        """
        user = User.query.filter_by(id=id).first()
        meters = Meter.query.with_parent(user).all()
        meters = list_to_array(meters)
        return custom_response(
            200,
            "{} meters".format(user.username),
            meters
        )


@ns.route('/last/<int:limit>')
@api.doc(security='apiKey')
class LastMetersApi(Resource):

    @jwt_required
    @requires_access_level(2)
    @api.doc(params={'limit': 'number of element to keep'})
    def get(self, limit):
        """
        Return the last n meters
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        meters = Meter.query.with_parent(current_user).limit(limit).all()
        meters = list_to_array(meters)
        return custom_response(
            200,
            "Last {} meters".format(limit),
            meters
        )
