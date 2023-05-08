from flask import Flask,Blueprint
from flask_restful import Api
from model import db
from flask_migrate import Migrate
from user_blueprint.user import Index,UserView,UpdateUser
from category_bluprint.category import CategoryView,UpdateCategory
from product_blueprint.product import  ProductView,ProductDetails
from address_blupeprint.address import AddressView,Addressdetails
from order_blueprint.order import OrderPlacement,OrderPlacementDetails
from order_item_blueprint.order_item import OrderItemDetails

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:123@localhost/demo'

db.init_app(app)
migrate=Migrate(app,db)


"""with app.app_context():
    db.create_all()"""
    
data_blueprint=Blueprint('data',__name__)

api=Api(data_blueprint)
app.register_blueprint(data_blueprint,url_prefix='/')

api.add_resource(Index,'/')
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
api.add_resource(OrderItemDetails,'/order_item')


if __name__=='__main__':
    app.run(debug=True, port=3000) 