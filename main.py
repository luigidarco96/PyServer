from flask import Flask
from database.db import initialise_db
from flask_restful import Api
from resources.routes import initialise_routes

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://luigi:luigi@localhost/piserver'

initialise_db(app, True)
initialise_routes(api)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
