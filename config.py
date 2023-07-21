from flask import Flask
import time,os
import functools
from flasgger import Swagger
from app.v1.views.swagger.swagger import swagger_config, template
from celery import Celery
from app.models.model import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api

app = Flask(__name__)

jwt = JWTManager()

api = Api(app)

db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

db_host = os.environ.get('DB_HOST', 'localhost')
db_username = os.environ.get('DB_USERNAME','myuser')
db_password = os.environ.get('DB_PASSWORD','password')
db_name = os.environ.get('DB_NAME','demo2')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"

app.config['JWT_SECRET_KEY'] = '1313'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

swagger = Swagger(app, config=swagger_config, template=template)
import logging

#Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create a file handler
handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

def measure_time(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        response = await func(*args, **kwargs)
        end_time = time.monotonic()
        logger.info(f'{func.__name__} took {end_time - start_time:.6f} seconds')
        return response
    return wrapper


from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def role_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                identity = get_jwt_identity()
                print(identity)
                if 'role_id' in identity and identity['role_id'] in permission:
                    return func(*args, **kwargs)
                else:
                    return {'message': 'Permission denied'}, 403
            except Exception as e:
                return {'message': 'Authentication required'}, 401
        return wrapper
    return decorator