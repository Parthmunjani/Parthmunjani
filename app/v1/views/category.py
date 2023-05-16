from flask import make_response, request
from app.v1.service.categorys import CategoryService
from flask_restful import Resource

class Categories(Resource):
    def get(self):
        try:
            response = CategoryService.get_all_categories()
            return make_response({"status":True,"details":response['detail']})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def post(self):
        try:
            data = request.get_json()
            response = CategoryService.create_category(data)
            return make_response({"status":True,"details":response['detail']})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

class Category(Resource):
    def get(self, id):
        try:
            response = CategoryService.get_category_by_id(id)
            return make_response({"status":True,"details":response['detail']})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def delete(self, id):
        try:
            response = CategoryService.delete_category(id)
            return make_response({"status":True,"details":response['detail']})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})
