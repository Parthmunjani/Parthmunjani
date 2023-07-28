from app.models.model import db,DBHandler
from datetime import datetime

class ProductModel(db.Model, DBHandler):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(), nullable=True, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, data):
        self.name = data.get('name')
        self.price = data.get('price', 0)
        self.category_id = data.get('category_id')
        self.created_at = datetime.utcnow()

    def to_json(self):
        data = {
            "name": self.name,
            "price": self.price,
            "category_id": self.category_id,
        }
        return data