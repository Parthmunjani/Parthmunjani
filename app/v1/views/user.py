from app.models.model import UserModel
from flask import make_response,request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from app.v1.service.user import UserService

class Users(Resource):
    def get(self):
        try:
            response = UserService.get_all_users()
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})
        
    def post(self):
        try:
            data = request.form.to_dict()
            file = request.files.get("id_proof_document")
            response = UserService.create_user(data, file)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

class User(Resource):
    def get(self, id):
        try:
            response = UserService.get_user(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def put(self, id):
        try:
            data = request.form.to_dict()
            response = UserService.update_user(id, data)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def delete(self, id):
        try:
            response = UserService.delete_user(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

class AuthLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            user = UserModel.query.filter_by(email=data['email']).first()
            if user and user.check_password(data['password']):
                access_token = create_access_token(identity=user.id)
                return make_response({"status":True,"access_token":access_token})
            else:
                return make_response({"status": False,"detail": "Invalid email or password"})
        except Exception as e:
            return make_response({"status": False,"detail":str(e)})