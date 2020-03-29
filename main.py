import argparse
import settings
from flask import Flask
from database.db import initialise_db
from api import api
from api.jwt_manager import initialise_jwt
from api.routes import initialise_routes

app = Flask(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

    flask_app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
    flask_app.config['JWT_BLACKLIST_ENABLED'] = settings.JWT_BLACKLIST_ENABLED
    flask_app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = settings.JWT_BLACKLIST_TOKEN_CHECKS


def initialize_app(flask_app):
    configure_app(flask_app)

    # Get arguments from cli
    parser = argparse.ArgumentParser(description='PiServer')
    parser.add_argument("--init", default=False, help="This initialise the database")

    args = parser.parse_args()
    init_db = args.init

    # Initialise DB
    if not init_db:
        initialise_db(app, False)
    else:
        initialise_db(app, True)

    # Initialise JWT
    initialise_jwt(app)

    # Initialise API
    api.init_app(app)
    initialise_routes(api)


def main():
    initialize_app(app)
    app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
