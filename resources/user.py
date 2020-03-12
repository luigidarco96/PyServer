from flask import Response, request
from database.db import db
from database.models.user import User
from flask_restful import Resource
from .utility import list_to_json
import json


class UsersApi(Resource):

    def get(self):
        users = User.query.all()
        users = list_to_json(users)
        return Response(users, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        user = User(
            username=body['username']
        )
        db.session.add(user)
        db.session.commit()
        id = user.id
        return {'id': str(id)}, 200


class UserApi(Resource):

    def get(self, id):
        user = User.query.filter_by(id=id).first()
        user = json.dumps(user.to_dict())
        return Response(user, mimetype="application/json", status=200)
