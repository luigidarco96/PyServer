from ..db import db
from passlib.hash import pbkdf2_sha256 as sha256

USER_ROLE = {
    'admin': 0,
    'family': 1,
    'user': 2
}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        dict = {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }
        return dict

    @classmethod
    def is_admin(cls, user):
        return user['role'] == USER_ROLE['admin']

    @classmethod
    def is_user(cls, user):
        return user['role'] == USER_ROLE['user']

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def __repr__(self):
        return '<User %r>' % self.username
