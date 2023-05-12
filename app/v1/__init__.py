from flask import Flask,Blueprint
from flask_restful import Api
from app.models.model import db
from flask_migrate import Migrate
from app.v1.user import Users,User
from app.v1.category import Categorys,Category
from app.v1.product import  Product,Products
from app.v1.address import AddressView,Address
from app.v1.order import *
from app.v1.order_item import OrderItemDetails

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123@localhost/demo'

db.init_app(app)
migrate=Migrate(app,db)


"""with app.app_context():
    db.create_all()"""
    
data_blueprint=Blueprint('data',__name__)

api=Api(data_blueprint)
app.register_blueprint(data_blueprint,url_prefix='/')


api.add_resource(Users,'/user')
api.add_resource(User,'/user/<int:id>/')
api.add_resource(Categorys,'/category')
api.add_resource(Category,'/category/<int:id>')
api.add_resource(Products,'/product')
api.add_resource(Product,'/product/<int:id>')
api.add_resource(AddressView,'/address')
api.add_resource(Address,'/address/<int:id>')
api.add_resource(Orders,'/order')
api.add_resource(Order,'/order/<int:id>')
api.add_resource(OrderStatus,'/order/<int:id>/status')
api.add_resource(OrderItemDetails,'/order_item')
api.add_resource(OrderStatusCounts, '/order/count/<int:id>')