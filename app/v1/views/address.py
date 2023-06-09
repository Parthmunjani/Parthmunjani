from flask_restful import Resource
from flask import make_response, request
from app.models.model import UserAddressModel
from app.v1.service.address import AddressService
from app.v1.service.data_service import DataService
from app.v1.validation.address import UserAddressSchema
from app.v1.schema.addressschema import user_address_schema
from flask_jwt_extended import jwt_required
from flasgger import swag_from

class Addresses(Resource):
    @swag_from({
        'tags': ['Addresses'],
        'summary': 'Get all addresses',
        'responses': {
            200: {
                'description': 'OK',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'boolean'},
                        'details': {'$ref': '#/definitions/AddressModel'}
                    }
                }
            }
        }
    })
    @jwt_required()
    def get(self):
        try:
            address_service,status_code=AddressService().get_all_addresses()
            return {"status":True,"details":address_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400

    @swag_from({
        'tags': ['Addresses'],
        'summary': 'Create a new address',
        'parameters': [
            {
                'in': 'body',
                'name': 'data',
                'description': 'Address data',
                'schema': {'$ref': '#/definitions/AddressModel'}
            }
        ],
        'responses': {
            200: {
                'description': 'OK',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'boolean'},
                        'details': {'type': 'string'}
                    }
                }
            }
        }
    })
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
            user_data = DataService(UserAddressModel).get_all_data(id=data.get('user_id'))
            if not user_data:
                return {"status": False, "detail": "User does not exist"}, 400
            response, status_code = address_service.create_address(data)
            return {"status": True, "details": response['detail']}, status_code
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
        
class Address(Resource):
    @swag_from({
        'tags': ['Addresses'],
        'summary': 'Get address by ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the address'
            }
        ],
        'responses': {
            200: {
                'description': 'OK',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'boolean'},
                        'details': {'$ref': '#/definitions/AddressModel'}
                    }
                }
            }
        }
    })
    @jwt_required()
    def get(self, id):
        try:
            address_service,status_code=AddressService().get_address_by_id(id)
            return {"status":True,"details":address_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400
        
    @swag_from({
        'tags': ['Addresses'],
        'summary': 'Update address by ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the address'
            },
            {
                'in': 'body',
                'name': 'data',
                'description': 'Address data',
                'schema': {'$ref': '#/definitions/AddressModel'}
            }
        ],
        'responses': {
            200: {
                'description': 'OK',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'boolean'},
                        'details': {'type': 'string'}
                    }
                }
            }
        }
    })    
    @jwt_required()
    def put(self, id):
        try:
            address_service=AddressService()
            data = request.get_json()
            response,status_code = address_service.update_address(id, data)
            return {"status":True,"details":response}, status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400

    @swag_from({
        'tags': ['Addresses'],
        'summary': 'Delete address by ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID of the address'
            }
        ],
        'responses': {
            200: {
                'description': 'OK',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'boolean'},
                        'details': {'type': 'string'}
                    }
                }
            }
        }
    })
    @jwt_required()
    def delete(self, id):
        try:
            address_service,status_code=AddressService().delete_address(id)
            return {"status":True,"details":address_service['detils']}, status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400 