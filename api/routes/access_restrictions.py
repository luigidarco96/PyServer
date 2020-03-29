from functools import wraps
from flask_jwt_extended import get_jwt_identity
from database.models.user import User


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_jwt_identity()
            current_user = User.find_by_username(user["username"])
            if not current_user:
                return {'message': "Permission denied. User not found"}, 401

            if current_user.role > access_level:
                return {'message': "Permission denied."}, 401

            return f(*args, **kwargs)
        return decorated_function
    return decorator
