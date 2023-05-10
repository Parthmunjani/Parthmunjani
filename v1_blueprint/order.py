from flask import make_response
from flask_restful import Resource,request
from model import OrderModel,OrderItemModel,CategoryModel,ProductModel

class OrderPlacement(Resource):
    def get(self):
        try:
            orders = OrderModel.query.all()
            if not orders:
                return make_response({"status":False,"detail":"No Data In Table"})
            data = [order.to_json(order) for order in orders]
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def post(self):
        try:
            data = request.get_json()
            create_order = OrderModel(data)
            OrderModel.add(create_order)
            data=create_order.to_json(create_order)
            return make_response({"status":True,"detail":"Your Order Placed Successfully"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
    
class OrderPlacementDetails(Resource):
    def get(self,id):
        try:
            orders = OrderModel.query.filter_by(user_id=id).all()
            if not orders:
                return make_response({"status": False, "detail": "No Orders Found"})
            order_list = []
            for order in orders:
                order_data = order.to_json(order)
                order_data['order_items'] = []
                order_items = OrderItemModel.query.filter_by(order_id=order.id).all()
                for item in order_items:
                    order_item_data = item.to_json(item)
                    order_data['order_items'].append(order_item_data)
                order_list.append(order_data)
            return make_response({"status": True, "detail": order_list})
        except Exception as e:
            return make_response({"status": False, "details": str(e)})

class OrderStatus(Resource):
    def get(self,id):
        try:
            order = OrderModel.query.get(id) 
            if not order:
                return make_response({"status": False, "details": "Order Not found"})
            data=order.to_json(order)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def put(self,id):
        try:
            status = request.json['status']
            order = OrderModel.query.get(id)
            if not order:
                return make_response({"status":False,'details': 'Order not found'})
            order.status=status
            OrderModel.put()
            return make_response({"status":True,"details":"Order status updated successfully"})
        except Exception as e:
            return make_response({'status':False,"details":str(e)})
        
class OrderStatusCounts(Resource):
    def get(self,id):
        try:
            category = OrderModel.query.get(id)
            if not category:
                return make_response({"status":False,"detail":'Category not found'})
            
            counts = {}
            for status in ['placed', 'paid', 'cancelled']:
                count = OrderModel.query.filter_by(status=status, order_id=id).count()
                counts[status] = count

            return make_response({"status":True,"details": counts})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})