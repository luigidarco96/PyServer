from flask import Response, request, abort
from flask_restplus import Resource
import time
import calendar
import os
import sys
import ml_resources.face_scrapper as fs
from deepface import DeepFace
from api import api

dir_name = os.path.dirname(sys.modules['__main__'].__file__)
image_save_path = dir_name + "/ml_resources/images/"
SAVE_IMAGES = True

ns = api.namespace('prediction', description='Operations related to image prediction')


@ns.route('')
class PredictionApi(Resource):

    def post(self):
        """
        Return the emotion prediction for the specified image
        """
        if not request.files:
            abort(400)

        image = request.files.get("image", "")

        timestamp = calendar.timegm(time.gmtime())
        image_name = str(timestamp) + ".jpg"
        image.save(os.path.join(image_save_path, image_name))

        status, new_face_path = fs.make_scraper(image_save_path + image_name)

        if not status:
            if not SAVE_IMAGES:
                os.remove(image_save_path + image_name)
            return new_face_path
        else:

            demography = "" # DeepFace.analyze(new_face_path, ["emotion"])
            if not SAVE_IMAGES:
                os.remove(image_save_path + image_name)
                os.remove(new_face_path)
            return demography
