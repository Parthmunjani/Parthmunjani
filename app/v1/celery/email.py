from config import app,celery,mail
from flask_restful import Resource,request
from flask_jwt_extended import JWTManager,jwt_required
from flask_mail import  Message
from datetime import timedelta, datetime

@celery.task()
def send_email(recipient, subject, body):
    with app.app_context():
        message = Message(subject=subject, recipients=[recipient], body=body)
        mail.send(message)


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
