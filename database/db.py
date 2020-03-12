from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def initialise_db(app, initialise):
    db.init_app(app)
    if initialise:
        with app.app_context():
            db.create_all()
            print("DB tables created")

