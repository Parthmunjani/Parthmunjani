from config import app,celery,mail
from flask_mail import Message


@celery.task()
def send_email(recipient, subject, body):
    try:
        with app.app_context():
            message = Message(subject=subject, recipients=[recipient], body=body)
            mail.send(message)
    except Exception as e:
        print("Error sending email:", e)


@celery.task()
def send_scheduled_email():
    recipient = 'parthmunjani1111@gmail.com'
    subject = 'Scheduled Email'
    body = 'How are you?'
    send_email(recipient, subject, body)
