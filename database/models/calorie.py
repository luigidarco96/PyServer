from ..db import db


class Calorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('calories', lazy=True))

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
            "timestamp": self.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
            "value": self.value,
            "user_id": self.user_id
        }
        return dict

    def __repr__(self):
        return '<Calorie %r>' % self.id
