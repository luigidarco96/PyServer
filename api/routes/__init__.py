from .auth import ns as auth_namespace
from .activity import ns as activity_namespace
from .calorie import ns as calorie_namespace
from .food import ns as food_namespace
from .heart_rate import ns as heart_rate_namespace
from .image import ns as image_namespace
from .meter import ns as meter_namespace
from .prediction import ns as prediction_namespace
from .step import ns as step_namespace
from .user import ns as user_namespace


def initialise_routes(api):
    api.add_namespace(auth_namespace)
    api.add_namespace(activity_namespace)
    api.add_namespace(calorie_namespace)
    api.add_namespace(food_namespace)
    api.add_namespace(image_namespace)
    api.add_namespace(heart_rate_namespace)
    api.add_namespace(meter_namespace)
    api.add_namespace(prediction_namespace)
    api.add_namespace(step_namespace)
    api.add_namespace(user_namespace)
