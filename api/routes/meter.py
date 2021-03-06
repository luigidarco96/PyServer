from flask import request
from database.models.user import User
from database.models.meter import Meter
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
                old_meter.update()
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


@ns.route('/user/<int:id>')
@api.doc(security='apiKey', params={'id': 'id of the user'})
class MetersByUserApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self, id):
        """
        Return all the meters for the specified user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])

        if current_user.is_admin() or current_user.has_child(id):
            user = User.query.filter_by(id=id).first()
            if user is None:
                return custom_response(
                    404,
                    "User {} not found".format(id)
                )
            meters = Meter.query.with_parent(user).all()
            meters = list_to_array(meters)
            return custom_response(
                200,
                "{} meters".format(user.username),
                meters
            )
        else:
            return custom_response(
                401,
                "Permission denied. User {} not a child".format(id)
            )

