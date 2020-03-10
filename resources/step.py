from flask import Response, request, jsonify
from flask_restful import Resource
from database.models.user import User
from database.models.step import Step


class StepsApi(Resource):

    def get(self, id):
        user = User.objects.get(id=id)
        steps = user.steps
        array = []
        for i, element in enumerate(steps):
            array.append(element.to_json())
        return array, 200

    def post(self, id):
        step = request.get_json()
        new_step = Step(value=step["value"])
        user = User.objects.get(id=id)
        user.steps.append(new_step)
        user.save()
        return "Success", 200
