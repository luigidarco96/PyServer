from ..db import db


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    calorie = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(240))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('foods', lazy=True))

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
            "datetime": self.datetime.strftime("%m/%d/%Y, %H:%M:%S"),
            "calorie": self.calorie,
            "image_path": self.image_path,
            "user_id": self.user_id
        }
        return dict

    def __repr__(self):
        return '<Food %r>' % self.id