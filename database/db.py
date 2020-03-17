from flask_sqlalchemy import SQLAlchemy
import sys

db = SQLAlchemy()


def initialise_db(app, initialise):
    db.init_app(app)
    if initialise:
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("DB tables created")
            sys.exit(0)

