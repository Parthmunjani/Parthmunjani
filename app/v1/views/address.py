from flask_restful import Resource
from flask import make_response, request
from app.v1.service.address import AddressService


class Addresses(Resource):
    def get(self):
        try:
            response = AddressService.get_all_addresses()
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def post(self):
        try:
            data = request.get_json()
            response = AddressService.create_address(data)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

class Address(Resource):
    def get(self, id):
        try:
            response = AddressService.get_address_by_id(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def put(self, id):
        try:
            data = request.get_json()
            response = AddressService.update_address(id, data)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def delete(self, id):
        try:
            response = AddressService.delete_address(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})