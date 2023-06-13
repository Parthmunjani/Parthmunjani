from flask import request
from flask_restful import Resource
from app.models.model import ProductModel,CategoryModel



class ProductSearch(Resource):
    def get(self):
        try:
            search_term = request.args.get('search_term')
            sort_order = request.args.get('sort_order')
            page = int(request.args.get('page', 1)) 
             
            category_query = CategoryModel.query.filter(CategoryModel.name.like('%' + search_term + '%'))
            category = category_query.first()
            
            if category:
                query = ProductModel.query.filter_by(category_id=category.id)
            else:
                query = ProductModel.query.filter(ProductModel.name.like('%' + search_term + '%'))

            if sort_order == '-':
                query = query.order_by(ProductModel.price.asc())
            elif sort_order == '+':
                query = query.order_by(ProductModel.price.desc())

            per_page = int(request.args.get('per_page', 10))
            offset = (page - 1) * per_page
            paginated_query = query.offset(offset).limit(per_page)
            results = paginated_query.all()

            if not results:
                return {"status": False, "detail": "Product Not Found"}

            serialized_results = [product.to_json() for product in results]
            return {"status": True, "details": serialized_results}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

"""class ProductSearch(Resource):
    def get(self):
        try:
            search_term = request.args.get('search_term')
            sort_order = request.args.get('sort_order')
            page = int(request.args.get('page', 1)) 
             
            query = ProductModel.query.filter((ProductModel.name.like('%' + search_term + '%')) |
                    (CategoryModel.name.like('%' + search_term + '%')))
            
            if sort_order == '-':
                query = query.order_by(ProductModel.price.asc())
            elif sort_order == '+':
                query = query.order_by(ProductModel.price.desc())

            per_page = int(request.args.get('per_page', 10))
            offset = (page - 1) * per_page # for product show in page 
            paginated_query = query.offset(offset).limit(per_page)
            results = paginated_query.all()
            if not results:
                return {"status": False, "detail": "Product Not Found"}
            serialized_results = [product.to_json() for product in results]
            return {"status": True, "details": serialized_results}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400"""
        


