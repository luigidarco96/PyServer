from flask import Response, request
from database.models.user import User
from database.models.step import Step
from database.models.meter import Meter
from database.models.calorie import Calorie
from database.models.heart_rate import HeartRate
from flask_restful import Resource


class UsersApi(Resource):

    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        user = User()
        user.username = body['username']
        user.steps = []
        user.meters = []
        user.calories = []
        user.heart_rate = []

        for i, step in enumerate(body['steps']):
            x = Step(value=step["value"])
            user.steps.append(x)

        for i, meter in enumerate(body['meters']):
            x = Meter(value=meter["value"])
            user.meters.append(x)

        for i, calorie in enumerate(body['calories']):
            x = Calorie(value=calorie["value"])
            user.calories.append(x)

        for i, heart_rate in enumerate(body['heart_rates']):
            x = HeartRate(value=heart_rate["value"])
            user.heart_rates.append(x)

        user.save()
        id = user.id
        return {'id': str(id)}, 200


class UserApi(Resource):

    '''
    def put(self, id):
        body = request.get_json()
        User.objects.get(id=id).update(**body)
        return '', 200

    def delete(self, id):
        user = User.objects.get(id=id).delete()
        return '', 200
    '''

    def get(self, id):
        user = User.objects.get(id=id).to_json()
        return Response(user, mimetype="application/json", status=200)
