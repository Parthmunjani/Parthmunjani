import os
from celery import Celery
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api
from datetime import timedelta
from app.models.model import db


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

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'parth.munjani@sculptsoft.com'
app.config['MAIL_PASSWORD'] = 'pcgrescgvnfaipuj'
app.config['MAIL_DEFAULT_SENDER'] = 'parth.munjani@sculptsoft.com'

app.config['JWT_SECRET_KEY'] = '1313'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

CELERYBEAT_SCHEDULE = {
    'send-scheduled-email': {
        'task': 'app.v1.celery.celery_send_email.send_scheduled_email',
        'schedule': timedelta(minutes=1),
    },
}

app.config['CELERY_BEAT_SCHEDULE'] = CELERYBEAT_SCHEDULE

celery.conf.beat_schedule = CELERYBEAT_SCHEDULE
celery.conf.timezone = 'UTC'

from app.v1.views.swagger.swagger import swagger_config, template
swagger = Swagger(app, config=swagger_config, template=template)
