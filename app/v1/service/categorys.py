from app.models.model import CategoryModel

class CategoryService:
    def get_all_categories():
        try:
            categories = CategoryModel.query.filter(CategoryModel.parent_id.is_(None)).all()
            result = []
            for category in categories:
                data = CategoryService.get_category_data(category)
                result.append(data)
            return {"status": True, "detail":result}
        except Exception as e:
            return {"status": False, "detail": str(e)}

    def get_category_data(category):
        data = category.to_json()
        data['total_products'] = len(category.products)
        child_categories = []
        for child in category.children:
            child_data = CategoryService.get_category_data(child)
            child_categories.append(child_data)
        data['child_categories'] = child_categories
        return data

    def create_category(data):
        try:
            parent_id = data.get('parent_id')
            create_category = CategoryModel(data, parent_id)
            CategoryModel.add(create_category)
            return {"status": True, "detail": "Category added successfully"}
        except Exception as e:
            return {"status": False, "detail": str(e)}

    def get_category_by_id(id):
        try:
            category = CategoryModel.query.get(id) 
            if not category:
                return {"status": False, "details": "Category Not Available"}
            data = category.to_json()
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}

    def delete_category(id):
        try:
            category = CategoryModel.query.get_or_404(id)
            CategoryModel.delete(category)
            return {"status": True, "detail": "Category Data Delete"}
        except Exception as e:
            return {"status": False, "detail": str(e)}