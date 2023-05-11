from flask import Flask,Blueprint
from flask_restful import Api
from api_excersice.models.model import db
from flask_migrate import Migrate
from api_excersice.v1.user import UserView,UpdateUser
from api_excersice.v1.category import CategoryView,UpdateCategory
from api_excersice.v1.product import  ProductView,ProductDetails
from api_excersice.v1.address import AddressView,Addressdetails
from api_excersice.v1.order import *
from api_excersice.v1.order_item import OrderItemDetails

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123@localhost/demo'

db.init_app(app)
migrate=Migrate(app,db)


"""with app.app_context():
    db.create_all()"""
    
data_blueprint=Blueprint('data',__name__)

api=Api(data_blueprint)
app.register_blueprint(data_blueprint,url_prefix='/')


api.add_resource(UserView,'/user')
api.add_resource(UpdateUser,'/user/<int:id>/')
api.add_resource(CategoryView,'/category')
api.add_resource(UpdateCategory,'/category/<int:id>')
api.add_resource(ProductView,'/product')
api.add_resource(ProductDetails,'/product/<int:id>')
api.add_resource(AddressView,'/address')
api.add_resource(Addressdetails,'/address/<int:id>')
api.add_resource(OrderPlacement,'/order')
api.add_resource(OrderPlacementDetails,'/order/<int:id>')
api.add_resource(OrderStatus,'/order/<int:id>/status')
api.add_resource(OrderItemDetails,'/order_item')
api.add_resource(OrderStatusCounts, '/order/count/<int:id>')