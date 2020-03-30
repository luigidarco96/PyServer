from flask import request, send_from_directory
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.routes.access_restrictions import requires_access_level
from database.models.user import User
import calendar
import time
import os
import sys
from api.utility import custom_response
import base64
from api import api
from settings import FLASK_SERVER_NAME

dir_name = os.path.dirname(sys.modules['__main__'].__file__)
image_save_path = dir_name + "/food_images/"

server_url = FLASK_SERVER_NAME

ns = api.namespace('images', description='Operations related to images')


@ns.route('')
@api.doc(security='apiKey')
class ImagesApi(Resource):

    @jwt_required
    @requires_access_level(2)
    def post(self):
        """
        Add a new image for the caller user
        """

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

        custom_link = "{}/images/{}/{}".format(server_url, current_user.id, image_name)
        return custom_response(
            200,
            "Image saved",
            custom_link
        )


@ns.route('/<int:user>/<string:image>')
class ImageApi(Resource):

    # @jwt_required
    # @requires_access_level(2)
    @api.doc(params={
        'user': 'id of the user',
        'image': 'name of the image'
    })
    def get(self, user, image):
        """
        Return the image requested
        """
        # current_user = User.find_by_username(get_jwt_identity()['username'])

        '''
        if not str(current_user.id) == user:
            return custom_response(
                401,
                "Permission denied"
            )
        '''

        current_dir = "{}{}".format(image_save_path, user)
        print(current_dir)
        print(image)

        return send_from_directory(
            current_dir,
            image
        )
