from flask_restful import Resource
from flask import make_response,request
from app.models.model import ApiPermission,RoleModel

class Api_Permission(Resource):
    def get(self):
        try:
            api_permission = ApiPermission.query.all()
            if not api_permission:
                return {"status":False,"detail":"No Data In Table"}, 400
            data = [api.to_json() for api in api_permission]
            return {"status":True,"detail":data}, 200
        except Exception as e:
            return {"status":False,"detail":str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            api = ApiPermission(data)
            ApiPermission.add(api)
            data = api.to_json()
            return {"status": True, "detail": data}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

class Role(Resource):
    def get(self):
        try:
            role = RoleModel.query.all()
            if not role:
                return {"status": False, "detail": "No Data In Table"}, 400
            data = [api.to_json() for api in role]
            return {"status": True, "detail": data}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

    def post(self):
        try:
            data = request.get_json()
            api = RoleModel(data)
            RoleModel.add(api)
            data = api.to_json()
            return {"status": True, "detail": data}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400