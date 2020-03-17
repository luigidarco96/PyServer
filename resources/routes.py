from .user import UsersAllApi, UsersApi, UserApi
from .auth import LoginApi, LogoutAccess, LogoutRefresh, RefreshToken
from .prediction import PredictionApi
from .step import StepsAllApi, StepsApi, StepApi
from .meter import MetersAllApi, MetersApi, MeterApi
from .calorie import CaloriesAllApi, CaloriesApi, CalorieApi
from .heart_rate import HeartRatesAllApi, HeartRatesApi, HeartRateApi


def initialise_routes(api):
    api.add_resource(LoginApi, '/login')
    api.add_resource(LogoutAccess, '/logout_access')
    api.add_resource(LogoutRefresh, '/logout_refresh')
    api.add_resource(RefreshToken, '/refresh_token')

    api.add_resource(UsersAllApi, '/users/all')
    api.add_resource(UsersApi, '/users')
    api.add_resource(UserApi, '/users/<id>')

    api.add_resource(StepsAllApi, '/steps/all')
    api.add_resource(StepsApi, '/steps')
    api.add_resource(StepApi, '/steps/<id>')

    api.add_resource(MetersAllApi, '/meters/all')
    api.add_resource(MetersApi, '/meters')
    api.add_resource(MeterApi, '/meters/<id>')

    api.add_resource(CaloriesAllApi, '/calories/all')
    api.add_resource(CaloriesApi, '/calories')
    api.add_resource(CalorieApi, '/calories/<id>')

    api.add_resource(HeartRatesAllApi, '/heart-rates/all')
    api.add_resource(HeartRatesApi, '/heart-rates')
    api.add_resource(HeartRateApi, '/heart-rates/<id>')

    api.add_resource(PredictionApi, '/prediction')
