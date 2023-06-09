from flask import make_response, request
from app.v1.service.categorys import CategoryService
from flask_restful import Resource
from app.v1.schema.catrgotyschema import category_schema
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.v1.views.swagger.swagger import route

class Categories(Resource):
    @swag_from(str(route)+"/category.yaml", methods=['GET'])
    @jwt_required()
    def get(self):
        try:
            categoty_service,status_code=CategoryService().get_all_categories()
            return {"status":True,"details":categoty_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400

    @swag_from(str(route)+"/category.yaml",methods=['POST'])
    def post(self):
        try:
            categoty_service=CategoryService()
            data = request.get_json()
            errors = []
            for field in category_schema["required"]:
                if field not in data:
                    errors.append(f"'{field}' is required.")
            if errors:
                return {"status": False, "details": errors}, 400
            response,status_code = categoty_service.create_category(data)
            return {"status":True,"details":response['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400

class Category(Resource):
    @swag_from(str(route)+"/category.yaml",methods=['GET'])
    @jwt_required()
    def get(self, id):
        try:
            categoty_service,status_code=CategoryService().get_category_by_id(id)
            return {"status":True,"details":categoty_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400
        
    @swag_from(str(route)+"/category.yaml",methods=['DELETE'])
    @jwt_required()
    def delete(self, id):
        try:
            categoty_service,status_code=CategoryService().delete_category(id)
            return {"status":True,"details":categoty_service['detail']}, status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400
