from flask import request
from database.models.user import User
from database.models.food import Food
from flask_restplus import Resource
from datetime import datetime
from api.utility import list_to_array
from api.routes.access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utility import custom_response
from api import api
from api.custom_request import food_data

ns = api.namespace('foods', description='Operation related to foods')


@ns.route('/all')
@api.doc(security='apiKey')
class FoodsAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        """
        Return all the foods
        """
        foods = Food.query.all()
        foods = list_to_array(foods)
        return custom_response(
            200,
            "All foods",
            foods
        )


@ns.route('')
@api.doc(security='apiKey')
class FoodsApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        """
        Return all the foods for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        foods = Food.query.with_parent(current_user).all()
        foods = list_to_array(foods)
        return custom_response(
            200,
            "Your foods",
            foods
        )

    @jwt_required
    @requires_access_level(2)
    @api.expect(food_data)
    def post(self):
        """
        Add a new food for the caller user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])
        food = request.get_json()
        new_food = Food(
            name=food['name'],
            datetime=datetime.now(),
            calorie=food['calorie'],
            image_path="",
            user=current_user
        )
        new_food.save()
        return custom_response(
            200,
            "Food saved",
            new_food.id
        )


@ns.route('/<int:id>')
@api.doc(security='apiKey')
class FoodApi(Resource):

    @jwt_required
    @requires_access_level(1)
    @api.doc(params={'id': 'id of the user'})
    def get(self, id):
        """
        Return all the foods for the specified user
        """
        user = User.query.filter_by(id=id).first()
        foods = Food.query.with_parent(user).all()
        foods = list_to_array(foods)
        return custom_response(
            200,
            "{} foods".format(user.username),
            foods
        )
