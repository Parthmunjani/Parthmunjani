from app.models.model import db,DBHandler


class RoleModel(db.Model,DBHandler):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255))
    def __init__(self, data):
        self.role_name = data.get("role_name")

    def to_json(self):
        data = {
            "id":self.id,
            "role_name": self.role_name,
        }
        return data