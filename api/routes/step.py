from flask import request
from database.models.user import User
from database.models.step import Step
from flask_restplus import Resource
from datetime import datetime
from api.utility import list_to_array
from api.routes.access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utility import custom_response
from api import api
from api.custom_request import fitness_data

ns = api.namespace('steps', description='Operations related to steps')


@ns.route('/all')
@api.doc(security='apiKey')
class StepsAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        """
        Return all the steps
        """
        steps = Step.query.all()
        steps = list_to_array(steps)
        return custom_response(
            200,
            "All steps",
            steps
        )


@ns.route('')
@api.doc(security='apiKey')
class StepsApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        """
        Return all the steps for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        steps = Step.query.with_parent(current_user).all()
        steps = list_to_array(steps)
        return custom_response(
            200,
            "Your steps",
            steps
        )

    @jwt_required
    @requires_access_level(2)
    @api.expect(fitness_data)
    def post(self):
        """
        Add new step for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        step = request.get_json()
        new_step = Step(
            timestamp=datetime.now(),
            value=step['value'],
            user=current_user
        )
        new_step.save()
        return custom_response(
            200,
            "Step added",
            new_step.id
        )


@ns.route('/<int:id>')
@api.doc(security='apiKey')
class StepApi(Resource):

    @jwt_required
    @requires_access_level(1)
    @api.doc(params={'id': 'id of user'})
    def get(self, id):
        """
        Return all the steps for the specified user
        """
        user = User.query.filter_by(id=id).first()
        steps = Step.query.with_parent(user).all()
        steps = list_to_array(steps)
        return custom_response(
            200,
            "{} steps".format(user.username),
            steps
        )
