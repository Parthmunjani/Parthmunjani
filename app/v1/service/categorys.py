from app.models.model import CategoryModel
from app.v1.service.data_service import DataService
from app.v1.schema.catrgotyschema import category_schema

class CategoryService:
    def get_all_categories(self):
        try:
            categories =CategoryModel.query.filter(CategoryModel.parent_id.is_(None)).all()
            result = []
            for category in categories:
                data = CategoryService.get_category_data(category)
                result.append(data)
            return {"status": True, "detail":result}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

    def get_category_data(category):
        data = category.to_json()
        data['total_products'] = len(category.products)
        child_categories = []
        for child in category.children:
            child_data = CategoryService.get_category_data(child)
            child_categories.append(child_data)
        data['child_categories'] = child_categories
        return data

    def create_category(self,data):
        try:
            parent_id = data.get('parent_id')
            
            create_category = CategoryModel(data, parent_id)
            CategoryModel.add(create_category)
            return {"status": True, "detail": "Category added successfully"}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

    def get_category_by_id(self,id):
        try:
            category_service=DataService(CategoryModel).get_all_data(id)
            if not category_service:
                return {"status": False, "details": "Category Not Available"}, 400
            return {"status": True, "detail": category_service}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

    def delete_category(self,id):
        try:
            category_service=DataService(CategoryModel).delete_data(id)
            return {"status": True, "detail": "Category Data Delete"}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400