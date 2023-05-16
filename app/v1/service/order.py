from app.models.model import OrderModel, OrderItemModel, CategoryModel
from flask import make_response
from sqlalchemy import func

class OrderService:
    def get_all_orders():
        try:
            orders = OrderModel.query.all()
            if not orders:
                return {"status": False, "detail": "No Data In Table"}
            data = [order.to_json(order) for order in orders]
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def create_order(data):
        try:
            create_order = OrderModel(data)
            OrderModel.add(create_order)
            data = create_order.to_json(create_order)
            return {"status": True, "detail": "Your Order Placed Successfully"}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def get_orders_by_user_id(id):
        try:
            orders = OrderModel.query.filter_by(user_id=id).all()
            if not orders:
                return {"status": False, "detail": "Orders Not Found"}
            
            order_list = []
            for order in orders:
                order_data = order.to_json(order)
                order_data['order_items'] = []
                order_items = OrderItemModel.query.filter_by(order_id=order.id).all()
                for item in order_items:
                    order_item_data = item.to_json()
                    order_data['order_items'].append(order_item_data)
                order_list.append(order_data)
            return {"status": True, "detail": order_list}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def get_order_status(id):
        try:
            order = OrderModel.query.get(id)
            if not order:
                return {"status": False, "details": "Order Not found"}
            
            data = order.to_json(order)
            return {"status": True, "detail": data}
        except Exception as e:
            return {"status": False, "detail": str(e)}
    
    def update_order_status(id, status):
        try:
            order = OrderModel.query.get(id)
            if not order:
                return {"status": False, "details": "Order not found"}
            
            order.status = status
            OrderModel.put()
            return {"status": True, "details": "Order status updated successfully"}
        except Exception as e:
            return {"status": False, "details": str(e)}
    
    def get_order_status_counts(id):
        try:
            category = CategoryModel.query.get(id)
            if not category:
                return {"status": False, "detail": 'Category not found'}
            
            counts = {}
            status_counts = (
                OrderModel.query.with_entities(OrderModel.status, func.count())
                .filter_by(category_id=id)
                .group_by(OrderModel.status)
                .all()
            )
            
            for status, count in status_counts:
                counts[status] = count
            
            return {"status": True, "details": counts}
        except Exception as e:
            return {"status": False, "detail": str(e)}
