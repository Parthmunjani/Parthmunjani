from flask import make_response, request
from app.v1.service.product import ProductService
from flask_restful import Resource
from app.v1.schema.productschema import product_schema
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.v1.views.swagger.swagger import route

class Products(Resource):
    print(route)
    @swag_from(str(route)+"/product/get_all.yaml")
    @jwt_required()
    def get(self):
        try:
            product_service,status_code=ProductService().all_product()
            return {"status":True,"details":product_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400
        
    @swag_from(str(route)+"/product/post_product.yaml")
    @jwt_required()        
    def post(self):
        try:
            product_service=ProductService()
            data = request.get_json()
            errors = []
            for field in product_schema["required"]:
                if field not in data:
                    errors.append(f"'{field}' is required.")
            if errors:
                return {"status": False, "details": errors}, 400
            response,status_code = product_service.new_product(data)
            return {"status":True,"details":response['detail']}, status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400

class Product(Resource):
    @swag_from(str(route)+"/product/get_by_id.yaml")
    @jwt_required()
    def get(self, id):
        try:
            product_service=ProductService()
            response, status_code = product_service.get_product(id)
            return {"status":True,"details":response['detail']}, status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400
     
    #@swag_from(str(route)+"/product.yaml", methods=["PUT"]) 
    @jwt_required()
    def put(self, id):
        try:    
            product_service=ProductService()
            data = request.get_json()
            response,status_code = product_service.update_product(id, data)
            return {"status":True,"details":response['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400
        
    @swag_from(str(route)+"/product/delete_by_id.yaml")    
    @jwt_required()    
    def delete(self, id):
        try:
            product_service,ststus_code=ProductService().delete_product(id)
            return {"status":True,"details":product_service['detail']},ststus_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400