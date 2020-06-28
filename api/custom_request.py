from flask_restplus import fields
from api import api

fitness_data = api.model('Fitness data', {
    'value': fields.Integer(readOnly=True, required=True, description="Value to save"),
})

activity_data = api.model('Activity Data', {
    'name': fields.String(readOnly=True, required=True, description="Name of the activity"),
    'datetime': fields.DateTime(readOnly=True, required=True, description="Activity date time"),
    'duration': fields.Integer(readOnly=True, required=True, description="Activity duration"),
})

food_data = api.model('Food Data', {
    'name': fields.String(readOnly=True, required=True, description="Name of the food"),
    'datetime': fields.DateTime(readOnly=True, required=True, description="Activity date time"),
    'calorie': fields.Integer(readOnly=True, required=True, description="Food calorie"),
    'image_path': fields.String(readOnly=True, required=True, description="Image path"),
})

login_data = api.model('Login Data', {
    'username': fields.String(readOnly=True, required=True, description="Username"),
    'password': fields.String(readOnly=True, required=True, description="Password"),
})

qr_data = api.model('QR Data', {
    'code': fields.String(readOnly=True, required=True, description="QR code")
})

user_data = api.model('User Data', {
    'full_name': fields.String(readOnly=True, required=True, description="Full Name"),
    'date_of_birth': fields.String(readOnly=True, required=True, description="Date of Birth"),
    'gender': fields.Integer(readOnly=True, required=True, description="Gender"),
    'weight': fields.Integer(readOnly=True, required=True, description="Weight"),
    'height': fields.Integer(readOnly=True, required=True, description="Activity date time")
})


