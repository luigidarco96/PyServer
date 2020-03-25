from flask import request
from database.models.user import User
from database.models.activity import Activity
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_array
from .access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utility import custom_response


class ActivitiesAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        activities = Activity.query.all()
        activities = list_to_array(activities)
        return custom_response(
            200,
            "All activities",
            activities
        )


class ActivitiesApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])
        activities = Activity.query.with_parent(current_user).all()
        activities = list_to_array(activities)
        return custom_response(
            200,
            "Your activities",
            activities
        )

    @jwt_required
    @requires_access_level(2)
    def post(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])
        activity = request.get_json()
        new_activity = Activity (
            name=activity['name'],
            datetime=datetime.now(),
            duration=activity['duration'],
            user=current_user
        )
        new_activity.save()
        return custom_response(
            200,
            "Activity added",
            new_activity.id
        )


class ActivityApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        activities = Activity.query.with_parent(user).all()
        activities = list_to_array(activities)
        return custom_response(
            200,
            "{} activities".format(user.username),
            activities
        )
