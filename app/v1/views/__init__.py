from flask import  Blueprint
from flask_restful import Api
from app.v1.views.user import Users, User, AuthLogin, TokenRefresh
from app.v1.views.category import Category, Categories
from app.v1.views.product import Product, Products
from app.v1.views.address import Addresses, Address
from app.v1.views.order import Orders, Order, OrderStatus, OrderStatusCounts
from app.v1.views.order_item import OrderItemDetails
from app.v1.views.role import Api_Permission,Role
from config import app
from app.v1.views.send_email import Email

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'parth.munjani@sculptsoft.com'
app.config['MAIL_PASSWORD'] = 'pcgrescgvnfaipuj'
app.config['MAIL_DEFAULT_SENDER'] = 'parth.munjani@sculptsoft.com'

data_blueprint = Blueprint('data', __name__)

api = Api(data_blueprint)
app.register_blueprint(data_blueprint, url_prefix='/')

api.add_resource(TokenRefresh, '/refresh')
api.add_resource(AuthLogin, '/auth/login')
api.add_resource(Users, '/user')
api.add_resource(User, '/user/<int:id>')
api.add_resource(Categories, '/category')
api.add_resource(Category, '/category/<int:id>')
api.add_resource(Products, '/product')
api.add_resource(Product, '/product/<int:id>')
api.add_resource(Addresses, '/address')
api.add_resource(Address, '/address/<int:id>')
api.add_resource(Orders, '/order')
api.add_resource(Order, '/order/<int:id>')
api.add_resource(OrderStatus, '/order/<int:id>/status')
api.add_resource(OrderItemDetails, '/order_item')
api.add_resource(OrderStatusCounts, '/order/count/<int:id>')
api.add_resource(Email, '/send-email')
api.add_resource(Api_Permission,'/api_permissions')
api.add_resource(Role,'/role')

