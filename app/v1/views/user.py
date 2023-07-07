from app.models.model import UserModel
from flask import make_response,request
from flask_restful import Resource
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from app.v1.service.user import UserService
from app.v1.schema.userschema import user_schema
from datetime import timedelta
from flask_restful_swagger import swagger
from flasgger import swag_from
from app.v1.views.swagger.swagger import route
from queue import Queue

class Users(Resource):
    @swag_from(str(route)+"/user/get_all.yaml")
    @jwt_required()
    async def get(self):
        try:
            async def get_users_async(result):
                result["data"] = await UserService().get_users()
            result = {}
            await get_users_async(result)
            if "data" in result:
                user_service, status_code = result["data"]
                return {"status": True, "details": user_service['detail']}, status_code
            else:
                return {"status": False, "detail": "Failed to get user data"}, 400
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
        
    # @swag_from(str(route)+"/user.yaml", methods=["POST"])
    async def post(self):
        try:
            user_service=UserService()
            data = request.form.to_dict()
            file = request.files.get("id_proof_document")
            errors = []
            for field in user_schema["required"]:
                if field not in data:
                    errors.append(f"'{field}' is required.")
            if errors:
                return {"status": False, "details": errors}, 400
            response,ststus_code = await user_service.add_user(data, file)
            return {"status":True,"details":response},ststus_code
        except Exception as e:
            return {"status":False,"detail":str(e)}, 400

class User(Resource):
    @swag_from(str(route)+"/user/get_by_id.yaml")
    @jwt_required()
    async def get(self, id):
        try:
            async def get_user_by_id_async(result):
                result["data"] = await UserService().get_user_by_id(id)
            result = {}
            await get_user_by_id_async(result)
            if "data" in result:
                user_service, status_code = result["data"]
                return {"status": True, "details": user_service['detail']}, status_code
            else:
                return {"status": False, "detail": "Failed to get user by ID"}, 400
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
          
    # @swag_from(str(route)+"/user.yaml", methods=["PUT"])   
    @jwt_required()
    def put(self, id):
        try:
            user_service=UserService()
            data = request.form.to_dict()
            response,ststus_code = user_service.update_user_details(id,data)
            return {"status":True,"details":response},ststus_code
        except Exception as e:
            return {"status":False,"detail":str(e)}, 400
          
    @swag_from(str(route)+"/user/delete_by_id.yaml")
    @jwt_required()
    def delete(self, id):
        try:
            user_service,ststus_code=UserService().remove_user(id)
            return {"status":True,"details":user_service},ststus_code
        except Exception as e:
            return {"status":False,"detail":str(e)}, 400

class AuthLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            user = UserModel.query.filter_by(email=data['email']).first()
            if user and user.check_password(data['password']):
                access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
                return make_response({"status": True, "access_token": access_token})
            else:
                return make_response({"status": False, "detail": "Invalid email or password"})
        except Exception as e:
            return make_response({"status": False, "detail": str(e)})
    
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=get_jwt_identity())
        return {'access_token': new_access_token}, 200