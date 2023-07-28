from app.models.model import db,DBHandler
from datetime import datetime


class OrderItemModel(db.Model, DBHandler):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('user_order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, data):
        self.order_id = data.get('order_id')
        self.product_id = data.get('product_id')
        self.quantity = data.get('quantity')

    def to_json(self):
        data = {
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        }
        return data