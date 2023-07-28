from flask import  request
from app.v1.service.order import OrderService
from flask_restful import Resource
from app.v1.schema.orderschema import order_schema
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.v1.views.swagger.swagger import route


class Orders(Resource):
    @swag_from(str(route)+"/order/get_all.yaml")
    @jwt_required()
    async def get(self):
        try:
            order_service,status_code = await OrderService().get_orders()
            return {"status":True,"details":order_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400

    def post(self):
        try:
            order_service = OrderService()
            data = request.get_json()
            errors = []
            for field in order_schema["required"]:
                if field not in data:
                    errors.append(f"'{field}' is required.")
            if errors:
                return {"status": False, "details": errors}, 400
            response,status_code = order_service.creates_order(data)
            return {"status":True,"details":response['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400


class Order(Resource):
    @swag_from(str(route)+"/order/get_by_id.yaml")
    @jwt_required()
    def get(self, id):
        try:
            order_service,status_code = OrderService().get_order(id)
            return {"status":True,"details":order_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400


class OrderStatus(Resource):
    @jwt_required()
    def get(self, id):
        try:
            order_service,status_code=OrderService().get_order_status(id)
            return {"status":True,"details":order_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400

    @jwt_required()
    def put(self, id):
        try:
            order_service=OrderService()
            data = request.get_json()
            status = data.get('status')
            response,status_code = order_service.update_order_status(id, status)
            return {"status":True,"details":response['detail']}, status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400


class OrderStatusCounts(Resource):
    @jwt_required()
    def get(self, id):
        try:
            order_service,status_code=OrderService().get_order_status_counts(id)
            return {"status":True,"details":order_service['detail']},status_code
        except Exception as e:
            return {"status":True,"detail":str(e)}, 400