from app.models.user import UserModel
from app.models.order_item import OrderItemModel
from app.models.order import OrderModel
from app.models.product import ProductModel
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from app.v1.service.data_service import DataService
import psycopg2


class UserService:
    async def get_users(self):
        try:
            all_service = await DataService(UserModel).get_all_data()
            return {"status": True, "detail": all_service}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def add_user(self,data,file):
        try:
            if not file:
                return {"status": False, "detail": "Document is required"}, 400
            
            filename = secure_filename(file.filename)
            if filename.split('.')[-1] != 'pdf':
                return {"status": False, "detail": "Only PDF documents are allowed"}, 400
            
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
            return {"status": True, "detail": response_data}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
                
    async def get_user_by_id(self, id):
        try:
            user = UserModel.query.get(id)
            if not user:
                return {"status": False, "detail": "User Not Registered"}, 400
            
            orders =  OrderModel.query.filter_by(user_id=id).all()
            order_details = []
            for order in orders:
                order_items = await OrderItemModel.query.filter_by(order_id=order.id).all()
                items = []
                for item in order_items:
                    product = await ProductModel.query.get(item.product_id)
                    product_data = {"name": product.name, "price": product.price, "quantity": item.quantity}
                    items.append(product_data)
                order_data = {"order_id": order.id, "total_price": order.total_price,
                            "payment_status": order.payment_status, "order_items": items}
                order_details.append(order_data)
            user_data = user.to_json()
            user_data["order_details"] = order_details
            return {"status": True, "detail": user_data}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

        
    def update_user_details(self,id,data):
        try:
            user = UserModel.query.filter_by(id=id).first()
            if not user:
                return {"status": False, "detail": "User Not Registered"}, 400
            
            user.name = data.get('name')
            user.email = data.get('email')
            user.phone_number = data.get('phone_number')
            user.modified_at = datetime.utcnow()
            UserModel.put()
            data = user.to_json()
            return {"status": True, "detail": data}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

    def remove_user(self, id):
        try:
            conn = psycopg2.connect(
                host='localhost',
                port='5432',
                database='demo2',
                user='myuser',
                password='password'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user WHERE id = %s", (id,))
            conn.commit()
            conn.close()
            # all_service = DataService(UserModel).delete_data(id)
            return {"status": True, "detail": "User Data Delete"}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

