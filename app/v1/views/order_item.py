from flask import make_response,request
from flask_restful import Resource
from app.models.model import OrderItemModel
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.v1.views.swagger.swagger import route

class OrderItemDetails(Resource):
    @swag_from(str(route)+"/order_item/get_all.yaml")
    @jwt_required()
    def get(self):
        try:
            order_iteam = OrderItemModel.query.all()
            if not order_iteam:
                return {"status":False,"detail":"No Data In Table"}, 400
            data = [order.to_json() for order in order_iteam]
            return {"status":True,"detail":data}, 200
        except Exception as e:
            return {"status":False,"detail":str(e)}, 400
    
    #@swag_from(str(route)+"/order_item.yaml", methods=['POST'])     
    def post(self):
        try:
            data=request.get_json()
            order_item = OrderItemModel(data)
            OrderItemModel.add(order_item)
            data=order_item.to_json()
            return {"status":True,"detail":data}, 200
        except Exception as e:
            return {"status":False,"detail":str(e)}, 400