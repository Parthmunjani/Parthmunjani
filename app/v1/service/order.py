from app.models.model import OrderModel, OrderItemModel, CategoryModel
from sqlalchemy import func
from app.v1.service.data_service import DataService
from flask import request
class OrderService:
    async def get_orders(self):
        try:
            all_service = await DataService(OrderModel).get_all_data()
            return {"status": True, "detail": all_service}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def creates_order(self,data):
        try:
            order_service=DataService(OrderModel).create_data(data)
            return {"status": True, "detail": "Your Order Placed Successfully"}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def get_order(self,id):
        try:
            orders = OrderModel.query.filter_by(user_id=id).all()
            if not orders:
                return {"status": False, "detail": "Orders Not Found"}, 400
            
            order_list = []
            for order in orders:
                order_data = order.to_json(order)
                order_data['order_items'] = []
                order_items = OrderItemModel.query.filter_by(order_id=order.id).all()
                for item in order_items:
                    order_item_data = item.to_json()
                    order_data['order_items'].append(order_item_data)
                order_list.append(order_data)
            return {"status": True, "detail": order_list}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def get_order_status(self, id):
        try:
            order = OrderModel.query.get(id)
            if not order:
                return {"status": False, "details": "Order Not found"}, 400
            
            data = order.to_json(order)
            return {"status": True, "detail": data}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
    
    def update_order_status(self, id, status):
        try:
            order = OrderModel.query.get(id)
            if not order:
                return {"status": False, "details": "Order not found"}, 400
            
            order.status = status
            OrderModel.put()
            return {"status": True, "details": "Order status updated successfully"}, 200
        except Exception as e:
            return {"status": False, "details": str(e)}, 400
    
    def get_order_status_counts(self, id):
        try:
            category = CategoryModel.query.get(id)
            if not category:
                return {"status": False, "detail": 'Category not found'}, 400
            
            counts = {}
            status_counts = (
                OrderModel.query.with_entities(OrderModel.status, func.count())
                .filter_by(category_id=id)
                .group_by(OrderModel.status)
                .all()
            )
            
            for status, count in status_counts:
                counts[status] = count
            
            return {"status": True, "detail": counts}, 200
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400
