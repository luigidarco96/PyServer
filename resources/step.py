from flask import Response, request
from database.db import db
from database.models.user import User
from database.models.step import Step
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_json


class StepsApi(Resource):
    def get(self):
        steps = Step.query.all()
        steps = list_to_json(steps)
        return Response(steps, mimetype="application/json", status=200)


class StepApi(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        steps = Step.query.with_parent(user).all()
        steps = list_to_json(steps)
        return Response(steps, mimetype="application/json", status=200)

    def post(self, id):
        user = User.query.filter_by(id=id).first()
        step = request.get_json()
        new_step = Step(
            timestamp=datetime.now(),
            value=step['value'],
            user=user
        )
        db.session.add(new_step)
        db.session.commit()
        return {'id': str(new_step.id)}, 200
