from flask import Response, request
from database.db import db
from database.models.user import User
from database.models.calorie import Calorie
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_json


class CaloriesApi(Resource):
    def get(self):
        calories = Calorie.query.all()
        calories = list_to_json(calories)
        return Response(calories, mimetype="application/json", status=200)


class CalorieApi(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        calories = Calorie.query.with_parent(user).all()
        calories = list_to_json(calories)
        return Response(calories, mimetype="application/json", status=200)

    def post(self, id):
        user = User.query.filter_by(id=id).first()
        calorie = request.get_json()
        new_calorie = Calorie(
            timestamp=datetime.now(),
            value=calorie['value'],
            user=user
        )
        db.session.add(new_calorie)
        db.session.commit()
        return {'id': str(new_calorie.id)}, 200
