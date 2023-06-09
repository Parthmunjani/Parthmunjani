from datetime import datetime
from app.models.model import ProductModel
from app.v1.service.data_service import DataService


class ProductService:    
    def all_product(self):
        try:
            all_service = DataService(ProductModel).get_all_data()
            return {"status": True, "detail": all_service}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def new_product(self,data):
        try:
            product_service=DataService(ProductModel).create_data(data)
            return {"status": True, "detail": product_service}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def get_product(self,id):
        try:
            product_service=DataService(ProductModel).get_all_data(id)
            if not product_service:
                return {"status": False, "details": "Product Not Found"}, 400
            return {"status": True, "detail": product_service}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
        
    def update_product(self,id, data):
        try:
            product = ProductModel.query.get(id)
            product.price = data.get('price')
            product.name = data.get('name')
            product.category_id = data.get('category_id')
            product.modified_at = datetime.utcnow()
            ProductModel.put()
            data = product.to_json()
            return {"status": True, "detail": data}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def delete_product(self,id):
        try:
            product_service=DataService(ProductModel).delete_data(id)
            return {"status": True, "detail": "Product Data Delete"}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
