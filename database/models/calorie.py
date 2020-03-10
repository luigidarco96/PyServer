import datetime
from ..db import db


class Calorie(db.EmbeddedDocument):
    timestamp = db.DateTimeField(default=datetime.datetime.now)
    value = db.IntField(required=True)
