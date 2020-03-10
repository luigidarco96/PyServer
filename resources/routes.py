from .user import UserApi, UsersApi
from .prediction import PredictionApi
from .step import StepsApi


def initialise_routes(api):
    # api.add_resource(UsersApi, '/users')
    # api.add_resource(UserApi, '/users/<id>')
    # api.add_resource(PredictionApi, '/prediction')
    api.add_resource(StepsApi, '/steps/<id>')
