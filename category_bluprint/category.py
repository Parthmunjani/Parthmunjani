from model import CategoryModel,db
from flask import make_response,request
from flask_restful import Resource
from datetime import datetime
from werkzeug.utils import secure_filename
from model import ProductModel
from sqlalchemy.orm import joinedload
class CategoryView(Resource):
    def get(self):
        try:
            categories = CategoryModel.query.filter(CategoryModel.parent_id.is_(None)).all()
            result = []
            for category in categories:
                data = self.get_category_data(category)
                result.append(data)
            return make_response({"details": True, "data": result})
        except Exception as e:
            return make_response({"status": False, "detail": str(e)})

    def get_category_data(self, category):
        data = category.to_json()
        data['total_products'] = len(category.products)
        child_categories = []
        for child in category.children:
            child_data = self.get_category_data(child)
            child_categories.append(child_data)
        data['child_categories'] = child_categories
        return data

    """def get(self): 
        try:
            categories = CategoryModel.query.filter(CategoryModel.parent_id.is_(None)).all()
            result = []
            for category in categories:
                data = category.to_json()
                data['total_products'] = len(category.products)
                child_categories = []
                for child in category.children:
                    child_data = child.to_json()
                    child_data['total_products'] = len(child.products)
                    grandchild_categories = []
                    for grandchild in child.children:
                        grandchild_data = grandchild.to_json()
                        grandchild_data['total_products'] = len(grandchild.products)
                        grandchild_categories.append(grandchild_data)
                    child_data['child_categories'] = grandchild_categories
                    child_categories.append(child_data)
                data['child_categories'] = child_categories
                result.append(data)
            return make_response({"details":True,"data":result})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})"""

    def post(self):
        try:
            data=request.get_json()
            parent_id = data.get('parent_id')
            parent = CategoryModel.query.filter_by(id=parent_id).first() if parent_id else None
            create_category = CategoryModel(data, parent)
            CategoryModel.add(create_category)
            data=create_category.to_json()
            return make_response({"status":True,"detail":"Category add Successfully"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
class UpdateCategory(Resource):
    def get(self,id):
        try:
            users = CategoryModel.query.get(id) 
            if not users:
                return make_response({"status": False, "details": "Category Not Available"})
            data = users.to_dict()
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})

    def delete(self,id):
        try:
            user = CategoryModel.query.get_or_404(id)
            CategoryModel.delete(user)
            return make_response({"Status":True,"detail":"Category Data Delete"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
