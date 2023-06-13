from flask import make_response, request
from app.v1.service.product import ProductService
from flask_restful import Resource
from app.v1.schema.productschema import product_schema
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.v1.views.swagger.swagger import route
from app.models.model import ProductModel,CategoryModel

class Products(Resource):
    #print(route)
    @swag_from(str(route)+"/product/get_all.yaml")
    @jwt_required()
    def get(self):
        try:
            search_term = request.args.get('search_term')
            sort_order = request.args.get('sort_order')
            page = int(request.args.get('page', 1))
             
            query = ProductModel.query
            if search_term:
                query = query.filter(
                    (ProductModel.name.like('%' + search_term + '%')) |
                    (ProductModel.category.has(CategoryModel.name.like('%' + search_term + '%')))
                )
            if sort_order == '-':
                query = query.order_by(ProductModel.price.asc())
            elif sort_order == '+':
                query = query.order_by(ProductModel.price.desc())

            per_page = int(request.args.get('per_page', 10))
            offset = (page - 1) * per_page # for product show in page
            paginated_query = query.offset(offset).limit(per_page)
            results = paginated_query.all()
            if not results:
                return {"status": False, "detail": "Product Not Found"},400

            serialized_results = [product.to_json() for product in results]
            return {"status": True, "details": serialized_results}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
        
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