from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialise_routes

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/myfit',
}

initialize_db(app)
initialise_routes(api)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
