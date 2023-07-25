import os
from app.models.model import db
from config import app


db_host = os.environ.get('DB_HOST', 'localhost')
db_username = os.environ.get('DB_USERNAME','myuser')
db_password = os.environ.get('DB_PASSWORD','password')
db_name = os.environ.get('DB_NAME','demo2')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
