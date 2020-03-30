from flask import request
from database.models.user import User
from database.models.activity import Activity
from flask_restplus import Resource
from datetime import datetime
from api.utility import list_to_array
from api.routes.access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utility import custom_response
from api import api
from api.custom_request import activity_data

ns = api.namespace('activities', description='Operations related to activities')


@ns.route('/all')
@api.doc(security='apiKey')
class ActivitiesAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        """
        Return all the activities
        """
        activities = Activity.query.all()
        activities = list_to_array(activities)
        return custom_response(
            200,
            "All activities",
            activities
        )


@ns.route('')
@api.doc(security='apiKey')
class ActivitiesApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        """
        Return all activities for the caller user
        """
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
    @api.expect(activity_data)
    def post(self):
        """
        Add a new activity for the caller user
        """
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


@ns.route('/<int:id>')
@api.doc(security='apiKey')
class ActivityApi(Resource):

    @jwt_required
    @requires_access_level(1)
    @api.doc(params={'id': 'id of user'})
    def get(self, id):
        """
        Return all the activities for the specified user
        """
        user = User.query.filter_by(id=id).first()
        activities = Activity.query.with_parent(user).all()
        activities = list_to_array(activities)
        return custom_response(
            200,
            "{} activities".format(user.username),
            activities
        )