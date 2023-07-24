from flask import make_response, request
from app.v1.service.product import ProductService
from flask_restful import Resource
from app.v1.schema.productschema import product_schema
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.v1.views.swagger.swagger import route
from app.models.model import ProductModel,CategoryModel
import psycopg2
from config import role_required
class Products(Resource):
    #print(route)
    @swag_from(str(route)+"/product/get_all.yaml")
    @jwt_required()
    @role_required([1])
    def get(self):
        try:
            conn = psycopg2.connect(
                host='localhost',
                port='5432',
                database='demo2',
                user='myuser',
                password='password'
            )
            cursor = conn.cursor()

            search_term = request.args.get('search_term')
            sort_order = request.args.get('sort_order')
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))

            query = """
                SELECT p.*
                FROM product p
                LEFT JOIN category c ON p.category_id = c.id
                WHERE 1 = 1
            """
            params = []

            if search_term:
                query += " AND (p.name ILIKE %s OR c.name ILIKE %s)"
                params.extend(['%' + search_term + '%', '%' + search_term + '%'])

            if sort_order == '+':
                query += " ORDER BY price ASC"
            elif sort_order == '-': 
                query += " ORDER BY price DESC"
            offset = (page - 1) * per_page
            query += f" OFFSET {offset} LIMIT {per_page}"
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            if not results:
                return {"status": False, "detail": "Product Not Found"}, 400
            serialized_results = [self._serialize_product(row) for row in results]
            return {"status": True, "details": serialized_results}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

    def _serialize_product(self, row):
        product = {
            "id": row[0],
            "name": row[1],
            #"category": row[1],
            "price": row[2]
        }
        return product


    @swag_from(str(route)+"/product/post_product.yaml")
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
            return {"status":False,"detail":str(e)}, 400

class Product(Resource):
    @swag_from(str(route)+"/product/get_by_id.yaml")
    @jwt_required()
    @role_required([2])
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
            return {"status":False,"detail":str(e)}, 400
        
    @swag_from(str(route)+"/product/delete_by_id.yaml")    
    @jwt_required()    
    def delete(self, id):
        try:
            product_service,ststus_code=ProductService().delete_product(id)
            return {"status":True,"details":product_service['detail']},ststus_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400