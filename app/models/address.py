from app.models.model import db,DBHandler
from datetime import datetime


class UserAddressModel(db.Model, DBHandler):
    __tablename__ = "user_address"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    street = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.street = data.get('street')
        self.state = data.get('state')
        self.zip = data.get('zip')

    def to_json(self):
        data = {
            "user_id": self.user_id,
            "street": self.street,
            "state": self.state,
            "zip": self.zip
        }
        return data