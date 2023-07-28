from datetime import datetime
from app.models.product import ProductModel
from app.v1.service.data_service import DataService
from flask import request
import sqlalchemy
from app.models.model import db
import psycopg2


class ProductService:    
    def all_product(self):
        try:
            all_service = DataService(ProductModel).get_all_data()
            return {"status": True, "detail": all_service}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def new_product(self,data):
        try:
            data=request.get_json()
            new_product = ProductModel(data)

            insert_query = sqlalchemy.text(""" INSERT INTO product (name, price, category_id, created_at, modified_at)VALUES (:name, :price, :category_id, :created_at, :modified_at)""")
            db.session.execute(
                insert_query,
                {
                    'name': new_product.name,
                    'price': new_product.price,
                    'category_id': new_product.category_id,
                    'created_at': new_product.created_at,
                    'modified_at': new_product.modified_at
                }
            )
            db.session.commit()
            product_data=new_product.to_json()
            #product_service=DataService(ProductModel).create_data(data)
            return {"status": True, "detail": product_data}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def get_product(self,id):
        try:
            conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='demo2',
            user='myuser',
            password='password'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product WHERE id = %s", (id,))
            product_service = cursor.fetchone()
            if not product_service:
                return {"status": False, "details": "Product Not Found"}, 400
            conn.close()
            product = ProductModel({
            'id': product_service[0],
            'name': product_service[1],
            'price': product_service[2],
            'category_id': product_service[3]
            })
            return {"status": True, "detail": product.to_json()}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
        
    def update_product(self,id, data):
        try:
            conn = psycopg2.connect(
                host='localhost',
                port='5432',
                database='demo2',
                user='my_user',
                password='password'
            )
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE product SET price = %s, name = %s, category_id = %s, modified_at = %s WHERE id = %s",
                (data.get('price'), data.get('name'), data.get('category_id'), datetime.utcnow(), id)
            )
            conn.commit()
            conn.close()
            updated_product = ProductModel.query.get(id)
            serialized_product = updated_product.to_json()
            return {"status": True, "detail": serialized_product}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def delete_product(self,id):
        try:
            conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='demo2',
            user='myuser',
            password='password'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM product WHERE id = %s", (id,))
            conn.commit()
            conn.close()
            #product_service=DataService(ProductModel).delete_data(id)
            return {"status": True, "detail": "Product Data Delete"}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
