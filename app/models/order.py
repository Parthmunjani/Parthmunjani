from app.models.model import db,DBHandler
from datetime import datetime


class OrderModel(db.Model, DBHandler):
    __tablename__ = 'user_order'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payment_status = db.Column(db.String(200), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('user_address.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    total_price = db.Column(db.Float())
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItemModel', backref='user_order')

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.payment_status = data.get('payment_status')
        self.category_id = data.get('category_id')
        self.total_price = data.get('total_price')
        self.address_id = data.get('address_id')
        self.status = data.get('status')

    def to_json(self, data):
        data = {
            "user_id": data.user_id,
            "total_price": data.total_price,
            "payment_status": data.payment_status,
            "status": data.status
        }
        return data