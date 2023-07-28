from app.models.model import db,DBHandler
from datetime import datetime

class CategoryModel(db.Model, DBHandler):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    children = db.relationship('CategoryModel', backref=db.backref('parent', remote_side=[id]))
    products = db.relationship('ProductModel', backref='category', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, data, parent=None):
        self.name = data.get('name')
        self.parent_id = data.get('parent_id')

    def to_json(self):
        data = {
            'id': self.id,
            'name': self.name,
        }
        if self.children:
            data['sub_category'] = [child.to_json() for child in self.children]
        return data