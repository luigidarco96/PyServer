from ..db import db
from datetime import datetime


class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    bmi_class = db.Column(db.String(30), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('personal_info', lazy=True))

    def save(self):
        self.bmi = self.weight / (self.height ** 2)
        self.timestamp = datetime.now()
        self.bmi_class = self.__bmi_classification()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __bmi_classification(self):
        if self.bmi <= 16:
            return "Severe Thinness"
        elif self.bmi <= 17:
            return "Moderate Thinness"
        elif self.bmi <= 18.5:
            return "Mild Thinness"
        elif self.bmi <= 25:
            return "Normal"
        elif self.bmi <= 30:
            return "Overweight"
        elif self.bmi <= 35:
            return "Obese Class I"
        elif self.bmi <= 40:
            return "Obese Class II"
        elif self.bmi > 40:
            return "Obese Class III"

    def to_dict(self):
        return {
            "id": self.id,
            "weight": self.weight,
            "height": self.height,
            "bmi": self.bmi,
            "bmi_class": self.bmi_class,
            "timestamp": self.timestamp.strftime("%d/%m/%Y, %H:%M:%S"),
            "user_id": self.user_id
        }

    def __repr__(self):
        return '<Personal Info %r>' % self.id
