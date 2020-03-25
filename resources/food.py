from flask import request
from database.models.user import User
from database.models.food import Food
from flask_restful import Resource
from datetime import datetime
from .utility import list_to_array
from .access_restrictions import requires_access_level
from flask_jwt_extended import jwt_required, get_jwt_identity
from .utility import custom_response


class FoodsAllApi(Resource):

    @jwt_required
    @requires_access_level(0)
    def get(self):
        foods = Food.query.all()
        foods = list_to_array(foods)
        return custom_response(
            200,
            "All foods",
            foods
        )


class FoodsApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
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
    def post(self):
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


class FoodApi(Resource):

    @jwt_required
    @requires_access_level(1)
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        foods = Food.query.with_parent(user).all()
        foods = list_to_array(foods)
        return custom_response(
            200,
            "{} foods".format(user.username),
            foods
        )
