from flask import send_from_directory, request
from flask_restplus import Resource
from database.models.user import User
from api.custom_request import qr_data
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from .access_restrictions import requires_access_level
from api import api
import qrcode
import calendar
import time
import os
import sys
import json
from cryptography.fernet import Fernet
from api.utility import custom_response

key = Fernet.generate_key()

dir_name = os.path.dirname(sys.modules['__main__'].__file__)
image_save_path = dir_name + "/qr_codes/"

ns = api.namespace('qrcode', "Opeartions related to QRCode")


@ns.route('/generate')
@api.doc(security='apiKey')
class QrCode(Resource):

    @jwt_required
    @requires_access_level(2)
    def post(self):
        """
        Return a new QRCode
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])

        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10,
                           border=4)
        qr.add_data(generate_content_qr_code(current_user))
        qr.make(fit=True)
        img = qr.make_image()

        # Save QRCode Image
        timestamp = calendar.timegm(time.gmtime())
        image_name = str(timestamp) + ".jpg"
        current_path = "{}/{}".format(image_save_path, image_name)

        img.save(current_path)

        return send_from_directory(
            image_save_path,
            image_name
        )


@ns.route('/verify')
@api.doc(security='apiKey')
@api.expect(qr_data)
class QrCodeVerify(Resource):

    @jwt_required
    @requires_access_level(2)
    def get(self):
        """
        Make the caller account a family member for code user
        """
        current_user = User.find_by_username(get_jwt_identity()['username'])

        body = request.get_json()
        code = body['code']

        code_user = decode_content_qr_code(code)
        child_user = User.query.filter_by(id=code_user['id']).first()

        if child_user is None:
            return custom_response(
                404,
                "User {} not found".format(id)
            )

        current_user.add_child(child_user)

        return custom_response(
            200,
            "User {} added to your family".format(child_user.username),
            child_user.id
        )


def generate_content_qr_code(current_user):
    qr_user = {
        'id': current_user.id,
        'username': current_user.username
    }
    qr_string = json.dumps(qr_user)
    f = Fernet(key)
    encrypted = f.encrypt(qr_string.encode())
    print(encrypted)
    return encrypted


def decode_content_qr_code(content):
    f = Fernet(key)
    decrypted = f.decrypt(content.encode())
    qr_user = json.loads(decrypted)
    return qr_user
