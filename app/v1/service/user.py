from app.models.model import UserModel,OrderModel,OrderItemModel,ProductModel
from datetime import datetime
from werkzeug.utils import secure_filename
import os

class UserService:
    def get_all_users():
        try:
            users = UserModel.query.all()
            if not users:
                return {"status": False, "detail": "User Not found"}
            data = [user.to_json() for user in users]
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def create_user(data, file):
        try:
            if not file:
                return {"status": False, "detail": "Document is required"}
            
            filename = secure_filename(file.filename)
            if filename.split('.')[-1] != 'pdf':
                return {"status": False, "detail": "Only PDF documents are allowed"}
            
            media_dir = "media"
            if not os.path.exists(media_dir):
                os.makedirs(media_dir)
            
            file_path = os.path.join("media", filename)
            file.save(file_path)

            data["id_proof_document"] = file_path
            create_user = UserModel(data)
            UserModel.add(create_user)
            user_data = create_user.to_json()
            response_data = {
                "status": True,
                "detail": "User created successfully",
                "user_data": user_data,
                "file_path": file_path
            }
            return {"status": True, "detail": response_data}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def get_user(id):
        try:
            user = UserModel.query.get(id)
            if not user:
                return {"status": False, "detail": "User Not Registered"}
            
            orders = OrderModel.query.filter_by(user_id=id)
            order_details = []
            for order in orders:
                order_items = OrderItemModel.query.filter_by(order_id=order.id)
                items = []
                for item in order_items:
                    product = ProductModel.query.get(item.product_id)
                    product_data = {"name": product.name, "price": product.price, "quantity": item.quantity}
                    items.append(product_data)
                order_data = {"order_id": order.id, "total_price": order.total_price,
                              "payment_status": order.payment_status, "order_items": items}
                order_details.append(order_data)
            user_data = user.to_json()
            user_data["order_details"] = order_details
            return {"status": True, "detail": user_data}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def update_user(id, data):
        try:
            user = UserModel.query.filter_by(id=id).first()
            if not user:
                return {"status": False, "detail": "User Not Registered"}
            
            user.name = data.get('name')
            user.email = data.get('email')
            user.phone_number = data.get('phone_number')
            user.modified_at = datetime.utcnow()
            UserModel.put()
            data = user.to_json()
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def delete_user(id):
        try:
            user = UserModel.query.get_or_404(id)
            UserModel.delete(user)
            return {"status": True, "detail": "User Data Delete"}
        except Exception as e:
            return {"status": False, "detail": str(e)}