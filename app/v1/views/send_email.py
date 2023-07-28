from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request
from app.v1.celery.celery_send_email import send_email

class Email(Resource):
    @jwt_required()
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