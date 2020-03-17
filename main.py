import argparse
from flask import Flask
from database.db import initialise_db
from flask_restful import Api
from resources.routes import initialise_routes
from resources.jwt_manager import initialise_jwt

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://luigi:luigi@localhost/piserver'

app.config['JWT_SECRET_KEY'] = 'luigiluigi123'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

parser = argparse.ArgumentParser(description='PiServer')
parser.add_argument("--init", default=False, help="This initialise the database")

args = parser.parse_args()
init_db = args.init

if not init_db:
    initialise_db(app, False)
else:
    initialise_db(app, True)
initialise_routes(api)
initialise_jwt(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
