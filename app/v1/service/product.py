from datetime import datetime
from app.models.model import ProductModel

class ProductService:
    def get_all_products():
        try:
            products = ProductModel.query.all()
            if not products:
                return {"status": False, "detail": "No Data In Table"}
            data = [product.to_json() for product in products]
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def add_product(data):
        try:
            add_product = ProductModel(data)
            ProductModel.add(add_product)
            return {"status": True, "detail": "Product Add Successfully"}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def get_product(id):
        try:
            product = ProductModel.query.get(id) 
            if not product:
                return {"status": False, "details": "Product Not Added"}
            data = product.to_json()
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def update_product(id, data):
        try:
            product = ProductModel.query.get(id)
            product.price = data.get('price')
            product.name = data.get('name')
            product.category_id = data.get('category_id')
            product.modified_at = datetime.utcnow()
            ProductModel.put()
            data = product.to_json()
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def delete_product(id):
        try:
            product = ProductModel.query.get_or_404(id)
            ProductModel.delete(product)
            return {"status": True, "detail": "Product Data Delete"}
        except Exception as e:
            return {"status": False, "detail": str(e)}
