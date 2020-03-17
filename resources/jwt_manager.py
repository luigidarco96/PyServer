from flask_jwt_extended import JWTManager
from database.models.revoked_token import RevokedToken

jwt = JWTManager()

def initialise_jwt(app):
    jwt.init_app(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)