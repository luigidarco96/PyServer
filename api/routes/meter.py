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
        new_meter = Meter(
            timestamp=datetime.now(),
            value=meter['value'],
            user=current_user
        )
        new_meter.save()
        return custom_response(
            200,
            "Mater added",
            new_meter.id
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
