from flask import request, send_from_directory
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .access_restrictions import requires_access_level
from database.models.user import User
import calendar
import time
import os
import sys
from .utility import custom_response
import base64

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

        data = request.get_json()
        image = base64.b64decode(data['image'])

        timestamp = calendar.timegm(time.gmtime())
        image_name = str(timestamp) + ".jpg"

        current_path = "{}/{}".format(current_dir, image_name)

        with open(current_path, 'wb') as f:
            f.write(image)

        custom_link = "http://localhost/images/{}/{}".format(current_user.id, image_name)
        return custom_response(
            200,
            "Image saved",
            custom_link
        )


class ImageApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self, user, id):
        current_user = User.find_by_username(get_jwt_identity()['username'])

        if not str(current_user.id) == user:
            return custom_response(
                401,
                "Permission denied"
            )

        current_dir = "{}{}".format(image_save_path, user)
        print(current_dir)
        print(id)

        return send_from_directory(
            current_dir,
            id
        )
