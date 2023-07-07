# from flask_mail import Message
# from flask import request
# from flask_restful import Resource
# from app.v1.views import app, mail, celery

# @celery.task
# def send_email(recipient, subject, body):
#     with app.app_context():
#         message = Message(subject=subject, recipients=[recipient], body=body)
#         mail.send(message)

# class Email(Resource):
#     def post(self):
#         try:
#             data = request.get_json()
#             recipient = data['recipient']
#             subject = data['subject']
#             body = data['body']
#             send_email.delay(recipient, subject, body)
#             return {'message': 'Email sent!'}
#         except Exception as e:
#              return {"status":False,"detail":str(e)}, 400
