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


