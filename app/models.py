from datetime import datetime

from app import db


class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column("event_id", db.Integer, primary_key=True)
    event_subject = db.Column('event_subject', db.String(255))
    event_content = db.Column('event_content', db.String(255))
    timestamp = db.Column('timestamp', db.DateTime)
    recipients = db.relationship("Recipient", backref="event")

    def __init__(self, event_id, event_subject, event_content, timestamp):
        self.event_id = event_id
        self.event_subject = event_subject
        self.event_content = event_content
        self.timestamp = timestamp


class Recipient(db.Model):
    __tablename__ = 'recipient'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(50))
    email = db.Column("email", db.String(50))
    event_id = db.Column("event_id", db.Integer, db.ForeignKey('event.event_id'))
    timestamp = db.Column("timestamp", db.DateTime)

    def __init__(self, name, email, event_id):
        self.name = name
        self.email = email
        self.event_id = event_id
        self.timestamp = datetime.today()


class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column("task_id", db.String(50), primary_key=True)
    event_id = db.Column("event_id", db.Integer)
    recipient_id = db.Column("recipient_id", db.Integer)

    def __init__(self, task_id, event_id, recipient_id):
        self.task_id = task_id
        self.event_id = event_id
        self.recipient_id = recipient_id


def get_all_events():
    """
    Queries all the Events from database
    """
    return Event.query.all()


def get_all_recipients():
    """
    Queries all the Recipients including corresponding Event subject the recipient is added to.
    """
    return db.session.query(Event.event_subject, Event.timestamp, Recipient).filter(Event.event_id == Recipient.event_id)


def get_event(event_id):
    """
    Queries a particular Event
    :return:
    """
    return Event.query.get_or_404(event_id)


def get_recipient(recipient_id):
    """
    Queries a particular Recipient
    """
    return Recipient.query.get_or_404(recipient_id)


def get_task_id(recipient_id):
    """
    Queries the task id
    """
    return db.session.query(Task.task_id).filter(Task.recipient_id == recipient_id).first()


def get_task_id_for_event(event_id):
    """
    Queries all the task id that have the same event id
    """
    return db.session.query(Task.task_id).filter(Task.event_id == event_id).all()


def get_all_recipient_for_event(event_id):
    return db.session.query(Recipient.id).filter(Recipient.event_id == event_id).all()


def get_all_email_for_event(event_id):
    return db.session.query(Recipient.email, Recipient.id).filter(Event.event_id == Recipient.event_id,
                                                                  Recipient.event_id == event_id).all()

