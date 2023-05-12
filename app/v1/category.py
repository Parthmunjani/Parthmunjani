from app.models.model import CategoryModel
from flask import make_response,request
from flask_restful import Resource

class Categorys(Resource):
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

    def post(self):
        try:
            data=request.get_json()
            parent_id = data.get('parent_id')
            parent = CategoryModel.query.filter_by(id=parent_id).first() if parent_id else None
            create_category = CategoryModel(data, parent)
            CategoryModel.add(create_category)
            data=create_category.to_json(create_category)
            return make_response({"status":True,"detail":"Category add Successfully"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
class Category(Resource):
    def get(self,id):
        try:
            category = CategoryModel.query.get(id) 
            if not category:
                return make_response({"status": False, "details": "Category Not Available"})
            data = category.to_dict()
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})

    def delete(self,id):
        try:
            category = CategoryModel.query.get_or_404(id)
            CategoryModel.delete(category)
            return make_response({"Status":True,"detail":"Category Data Delete"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
