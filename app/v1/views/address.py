from flask_restful import Resource
from flask import  request
from app.v1.service.address import AddressService
from app.v1.schema.addressschema import user_address_schema
from flask_jwt_extended import jwt_required,get_jwt_identity
from flasgger import swag_from
from app.v1.views.swagger.swagger import route
from decorators import measure_time,role_required


class Addresses(Resource):
    @swag_from(str(route)+"/address/get_all.yaml")
    @jwt_required()
    @measure_time
    @role_required(["admin"])
    async def get(self):
        try:
            current_user = get_jwt_identity()
            address_service,status_code= await AddressService().get_all_addresses()
            return {"status":True,"details":address_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400

    @swag_from(str(route)+"/address/post_address.yaml")
    def post(self):
        try:
            address_service = AddressService()
            data = request.get_json()
            errors = []
            for field in user_address_schema["required"]:
                if field not in data:
                    errors.append(f"'{field}' is required.")
            if errors:
                return {"status": False, "details": errors}, 400
            """user_data = DataService(UserAddressModel).get_all_data(id=data.get('user_id'))
            if not user_data:
                return {"status": False, "detail": "User does not exist"}, 400"""
            response, status_code = address_service.create_address(data)
            return {"status": True, "details": response['detail']}, status_code
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400


class Address(Resource):
    @swag_from(str(route)+"/address/get_by_id.yaml")
    @jwt_required()
    def get(self, id):
        try:
            address_service,status_code=AddressService().get_address_by_id(id)
            return {"status":True,"details":address_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400
        
       
    @jwt_required()
    def put(self, id):
        try:
            address_service=AddressService()
            data = request.get_json()
            response,status_code = address_service.update_address(id, data)
            return {"status":True,"details":response}, status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400

    @swag_from(str(route)+"/address/delete_by_id.yaml")
    @jwt_required()
    def delete(self, id):
        try:
            address_service,status_code=AddressService().delete_address(id)
            return {"status":True,"details":address_service['detils']}, status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400 
