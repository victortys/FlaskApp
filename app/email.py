import pytz

from datetime import datetime
from flask_mail import Message
from models import Event, Task
from app import mail, celery, db


def send_email(event_id, user_mail, recipient_id):
    """
    Sends the email to the recipient according to the event subject and content saved
    """
    selected_event = Event.query.filter_by(event_id=event_id).first()

    # Store the content of the mail in a dict
    msg = {
            'recipient': [user_mail],
            'subject': selected_event.event_subject,
            'content': selected_event.event_content
        }

    # Localise the date to be parse to the celery worker
    date = selected_event.timestamp
    timezone = pytz.timezone("Asia/Singapore")
    eta_date = timezone.localize(date)
    if date > datetime.now():
        email = send_async_email.apply_async(args=[msg], eta=eta_date)

        # save the task id, event id and recipient id
        save_task = Task(email.id, event_id, recipient_id)
        db.session.add(save_task)
        db.session.commit()


@celery.task
def revoke_task(task_id):
    # revoke task from celery
    celery.control.revoke(task_id)


@celery.task
def send_async_email(msg):
    mail_msg = Message(msg['subject'], recipients=msg['recipient'])
    mail_msg.body = msg['content']
    mail.send(mail_msg)