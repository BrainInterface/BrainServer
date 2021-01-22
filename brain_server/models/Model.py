from models import db


class Model(db.Model):
    """
    Represents a ML-model.
    """
    id = db.Column(db.Integer, index=True, primary_key=True, unique=True)
    model_type = db.Column(db.text)
    path = db.Column(db.text, unique=True)
