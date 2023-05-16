from flask import make_response, request
from app.v1.service.product import ProductService
from flask_restful import Resource

class Products(Resource):
    def get(self):
        try:
            response = ProductService.get_all_products()
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})
            
    def post(self):
        try:
            data = request.get_json()
            response = ProductService.add_product(data)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

class Product(Resource):
    def get(self, id):
        try:
            response = ProductService.get_product(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})
            
    def put(self, id):
        try:
            data = request.get_json()
            response = ProductService.update_product(id, data)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})
        
    def delete(self, id):
        try:
            response = ProductService.delete_product(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})