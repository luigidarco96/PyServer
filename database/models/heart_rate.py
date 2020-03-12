from ..db import db


class HeartRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('heartrates', lazy=True))

    def __repr__(self):
        return '<Calorie %r>' % self.id

    def to_dict(self):
        dict = {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"),
            "value": self.value,
            "user_id": self.user_id
        }
        return dict

