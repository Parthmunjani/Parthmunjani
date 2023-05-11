from flask import make_response,request
from flask_restful import Resource
from model import OrderItemModel

class OrderItemDetails(Resource):
    def get(self):
        try:
            order_iteam = OrderItemModel.query.all()
            if not order_iteam:
                return make_response({"status":False,"detail":"No Data In Table"})
            data = [user.to_json(user) for user in order_iteam]
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def post(self):
        try:
            data=request.get_json()
            order_item = OrderItemModel(data)
            OrderItemModel.add(order_item)
            data=order_item.to_json(order_item)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})