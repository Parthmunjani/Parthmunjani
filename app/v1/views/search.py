from flask import request
from flask_restful import Resource
from app.models.model import ProductModel

class ProductSearch(Resource):
    def get(self):
        try:
            search_term = request.args.get('search_term')
            sort_order = request.args.get('sort_order')
            page = int(request.args.get('page', 1)) 
             
            query = ProductModel.query.filter(ProductModel.name.like('%' + search_term + '%'))
            if sort_order == 'low_to_high':
                query = query.order_by(ProductModel.price.asc())
            elif sort_order == 'high_to_low':
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
            return {"status": False, "detail": str(e)}, 400
        
"""class ProductSearch(Resource):
    def get(self):
        try:
            search_term = request.args.get('search_term')
            sort_order = request.args.get('sort_order')
            page = int(request.args.get('page', 1))
            #print(sort_order)
            query = ProductModel.query.filter(ProductModel.name.like('%'+search_term+'%'))
            #print(query)
            if sort_order == 'low_to_high':
                #print(sort_order)
                query = query.order_by(ProductModel.price.asc())
            elif sort_order == 'high_to_low':
                #print(sort_order)
                query = query.order_by(ProductModel.price.desc())
            results = query.all()
            #print(results)
            if not results:
                return {"status": False, "detail": "Product Not Found"}
            serialized_results = [product.to_json() for product in results]
            return {"status": True, "details": serialized_results}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400"""

