from .user import UserApi, UsersApi
from .prediction import PredictionApi
from .step import StepsApi, StepApi
from .meter import MetersApi, MeterApi
from .calorie import CaloriesApi, CalorieApi
from .heart_rate import HeartRatesApi, HeartRateApi


def initialise_routes(api):
    api.add_resource(UsersApi, '/users')
    api.add_resource(UserApi, '/users/<id>')
    api.add_resource(StepsApi, '/steps')
    api.add_resource(StepApi, '/steps/<id>')
    api.add_resource(MetersApi, '/meters')
    api.add_resource(MeterApi, '/meters/<id>')
    api.add_resource(CaloriesApi, '/calories')
    api.add_resource(CalorieApi, '/calories/<id>')
    api.add_resource(HeartRatesApi, '/heart-rates')
    api.add_resource(HeartRateApi, '/heart-rates/<id>')
    api.add_resource(PredictionApi, '/prediction')
