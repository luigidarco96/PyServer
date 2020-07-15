from ..db import db


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('activities', lazy=True))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def to_dict(self):
        dict = {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime.strftime("%d/%m/%Y, %H:%M:%S"),
            "duration": self.duration,
            "user_id": self.user_id
        }
        return dict

    def __repr__(self):
        return '<Activity %r>' % self.id