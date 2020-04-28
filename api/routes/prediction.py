from flask import Response, request, abort
from flask_restplus import Resource
from settings import SAVE_IMG
from api.utility import custom_response
import time
import calendar
import os
import sys
from ml_resources.e_recognition import make_scraper, predict_emotion
from api import api

dir_name = os.path.dirname(sys.modules['__main__'].__file__)
image_save_path = dir_name + "/ml_resources/images/"

ns = api.namespace('emotion-recognition', description='Operations related to emotion recognition')


@ns.route('')
class PredictionApi(Resource):

    def post(self):
        """
        Return the emotion predicted for the specified image
        """
        if not request.files:
            abort(400)

        image = request.files.get("image", "")

        timestamp = calendar.timegm(time.gmtime())
        image_name = str(timestamp) + ".jpg"
        image.save(os.path.join(image_save_path, image_name))

        new_face_path = make_scraper(image_save_path + image_name)

        if new_face_path is None:
            if not SAVE_IMG:
                os.remove(image_save_path + image_name)
            return custom_response(
                404,
                "No face found"
            )
        else:
            prediction = predict_emotion(new_face_path)
            if not SAVE_IMG:
                os.remove(image_save_path + image_name)
                os.remove(new_face_path)
            if prediction is None:
                return custom_response(
                    404,
                    "No emotion recognise"
                )
            else:
                return custom_response(
                    200,
                    prediction
                )
