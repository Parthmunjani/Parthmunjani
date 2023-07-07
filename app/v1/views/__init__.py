from celery import Celery
from flask import Flask, Blueprint, request
from flask_restful import Api, Resource
from app.models.model import db
from flask_migrate import Migrate
from app.v1.views.user import Users, User, AuthLogin, TokenRefresh
from app.v1.views.category import Category, Categories
from app.v1.views.product import Product, Products
from app.v1.views.address import Addresses, Address
from app.v1.views.order import Orders, Order, OrderStatus, OrderStatusCounts
from app.v1.views.order_item import OrderItemDetails
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from app.v1.views.swagger.swagger import swagger_config, template
from datetime import timedelta, datetime
import os
from flask_mail import Mail, Message
from celery.schedules import crontab

db_host = os.environ.get('DB_HOST')
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

jwt = JWTManager()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
app.config['JWT_SECRET_KEY'] = '1313'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'parth.munjani@sculptsoft.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = 'parth.munjani@sculptsoft.com'

api = Api(app)
jwt = JWTManager(app)

db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

swagger = Swagger(app, config=swagger_config, template=template)


@celery.task()
def send_email(recipient, subject, body):
    with app.app_context():
        message = Message(subject=subject, recipients=[recipient], body=body)
        mail.send(message)


class Email(Resource):
    def post(self):
        try:
            data = request.get_json()
            recipient = data['recipient']
            subject = data['subject']
            body = data['body']
            send_email.delay(recipient, subject, body)
            return {'message': 'Email sent!'}
        except Exception as e:
            return {"status": False, "detail": str(e)}, 400

@celery.task()
def send_scheduled_email():
    recipient = 'parthmunjani1111@gmail.com'
    subject = 'Scheduled Email'
    body = 'How are you?'
    send_email(recipient, subject, body)

CELERYBEAT_SCHEDULE = {
    'send-scheduled-email': {
        'task': 'app.v1.views.send_scheduled_email',
        'schedule': timedelta(minutes=1),
    },
}

app.config['CELERY_BEAT_SCHEDULE'] = CELERYBEAT_SCHEDULE

celery.conf.beat_schedule = CELERYBEAT_SCHEDULE
celery.conf.timezone = 'UTC'


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


