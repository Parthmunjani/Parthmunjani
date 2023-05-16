from flask import make_response, request
from app.v1.service.order import OrderService
from flask_restful import Resource

class Orders(Resource):
    def get(self):
        try:
            response = OrderService.get_all_orders()
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def post(self):
        try:
            data = request.get_json()
            response = OrderService.create_order(data)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

class Order(Resource):
    def get(self, id):
        try:
            response = OrderService.get_orders_by_user_id(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def put(self, id):
        try:
            data = request.get_json()
            response = OrderService.update_order(id, data)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def delete(self, id):
        try:
            response = OrderService.delete_order(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

class OrderStatus(Resource):
    def get(self, id):
        try:
            response = OrderService.get_order_status(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

    def put(self, id):
        try:
            data = request.get_json()
            status = data.get('status')
            response = OrderService.update_order_status(id, status)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})

class OrderStatusCounts(Resource):
    def get(self, id):
        try:
            response = OrderService.get_order_status_counts(id)
            return make_response({"status":True,"details":response})
        except Exception as e:
            return make_response({"status":True,"detail":str(e)})