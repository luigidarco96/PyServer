from flask import Response, request
from database.models.user import User
from database.models.step import Step
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_json
from .access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity


class StepsAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        steps = Step.query.all()
        steps = list_to_json(steps)
        return Response(steps, mimetype="application/json", status=200)


class StepsApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])
        steps = Step.query.with_parent(current_user).all()
        steps = list_to_json(steps)
        return Response(steps, mimetype="application/json", status=200)

    @jwt_required
    @requires_access_level(2)
    def post(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])
        step = request.get_json()
        new_step = Step(
            timestamp=datetime.now(),
            value=step['value'],
            user=current_user
        )
        new_step.save()
        return {'id': str(new_step.id)}, 200


class StepApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        steps = Step.query.with_parent(user).all()
        steps = list_to_json(steps)
        return Response(steps, mimetype="application/json", status=200)

