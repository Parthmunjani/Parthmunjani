from app.models.model import db,DBHandler

class ApiPermission(db.Model,DBHandler):
    __tablename__ = 'api_permissions'

    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(255))
    method = db.Column(db.String(10))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('RoleModel', backref='permissions')
    def __init__(self, data):
        self.api_name = data.get("api_name")
        self.method = data.get("method")
        self.role_id = data.get("role_id")

    def to_json(self):
        data = {
            "api_name": self.api_name,
            "method": self.method,
            "role_id": self.role_id,
        }
        return data
