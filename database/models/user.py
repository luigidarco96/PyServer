from ..db import db
from .step import Step
from .calorie import Calorie
from .meter import Meter
from .heart_rate import HeartRate


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    steps = db.ListField(db.EmbeddedDocumentField(Step)) # db.EmbeddedDocumentListField(Step)
    meters = db.EmbeddedDocumentListField(Meter)
    calories = db.EmbeddedDocumentListField(Calorie)
    heart_rates = db.EmbeddedDocumentListField(HeartRate)
