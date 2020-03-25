from flask import Flask, Response, request, send_file
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .access_restrictions import requires_access_level
from database.models.user import User
import calendar
import time
import os
import sys

dir_name = os.path.dirname(sys.modules['__main__'].__file__)
image_save_path = dir_name + "/food_images/"


class ImagesApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def post(self):
        current_user = User.find_by_username(get_jwt_identity()['username'])

        current_dir = "{}{}/".format(image_save_path, current_user.id)

        if not os.path.exists(current_dir):
            os.makedirs(current_dir, exist_ok=True)

        image = request.files.get("image", "")

        timestamp = calendar.timegm(time.gmtime())
        image_name = str(timestamp) + ".jpg"
        image.save(os.path.join(current_dir, image_name))

        custom_link = "localhost/images/{}/{}".format(current_user.id, image_name)
        return custom_link, 200


class ImageApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self, user, id):
        current_user = User.find_by_username(get_jwt_identity()['username'])

        if not str(current_user.id) == user:
            return {'message': 'Permission denied'}, 401

        current_dir = "{}{}/{}".format(image_save_path, current_user.id, id)

        return Response(send_file(current_dir), mimetype='image/jpg', status=200)
