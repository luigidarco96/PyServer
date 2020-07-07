from ..db import db
from passlib.hash import pbkdf2_sha256 as sha256

USER_ROLE = {
    'admin': 0,
    'family': 1,
    'user': 2
}

groups = db.Table(
    'groups',
    db.Column('parent_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('children_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.Integer, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    family_members = db.relationship(
        'User',
        secondary=groups,
        primaryjoin=(groups.c.parent_id == id),
        secondaryjoin=(groups.c.children_id == id),
        backref=db.backref('parents', lazy='dynamic'),
        lazy='dynamic'
    )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def is_admin(self):
        return self.role == USER_ROLE['admin']

    def add_child(self, child):
        if child not in self.family_members:
            self.convert_to_family()
            self.family_members.append(child)
            db.session.commit()

    def has_child(self, child_id):
        child = self.family_members.filter_by(id=child_id).first()
        if child is None:
            return False
        else:
            return True

    def convert_to_family(self):
        if self.role == USER_ROLE['user']:
            self.role = USER_ROLE['family']

    def to_dict(self):
        dict = {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "full_name": self.full_name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth.strftime("%d/%m/%Y"),
        }
        return dict

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
