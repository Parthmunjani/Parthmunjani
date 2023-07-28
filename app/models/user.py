from flask_sqlalchemy import SQLAlchemy
from flask import request, make_response
from werkzeug.utils import secure_filename
from datetime import datetime
from uuid import uuid4
import os
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.model import db,DBHandler


class UserModel(db.Model, DBHandler):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), nullable=False, default=str(uuid4()))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    id_proof_document = db.Column(db.LargeBinary())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('RoleModel')
    def __init__(self,data):
        self.name=data.get("name")
        self.email=data.get("email")
        self.phone_number=data.get("phone_number")
        self.set_password(data.get("password"))
        self.role_id=data.get("role_id")

        file = request.files.get("id_proof_document")
        if file:
            filename = secure_filename(file.filename)
            try:
                file.save(os.path.join("media", filename))
                with open(os.path.join("media", filename), "rb") as f:
                    self.id_proof_document = f.read()
            except Exception as e:
                return make_response({"status":False,"details":str(e)})



    @property
    def role_name(self):
        # Access the role_name from the associated RoleModel
        if self.role:
            return self.role.role_name
        return None

    def set_password(self, password):
        hashed_password = generate_password_hash(password)
        self.password = hashed_password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        data = {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role_id":self.role_id,
        }
        return data