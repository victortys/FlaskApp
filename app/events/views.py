from __future__ import print_function

from flask import render_template, url_for, redirect, flash
from . import events
from forms import SaveEventForm

from app import db
from ..email import revoke_task, send_email
from ..models import Event, get_all_events, get_event, get_task_id_for_event, get_all_recipient_for_event, get_recipient, get_all_email_for_event


@events.route('/save_event', methods=['GET', 'POST'])
def save_event():
    """
    Add an event to the database
    """
    form = SaveEventForm()
    if form.validate_on_submit():
        print(form.timestamp.data)
        email_event = Event(form.event_id.data,
                            form.event_subject.data, 
                            form.event_content.data, 
                            form.timestamp.data)
        # add new event to database
        db.session.add(email_event)
        db.session.commit()
        flash('You have successfully save a new event!')

        # redirect to home page
        return redirect(url_for('events.show_events'))

    # load save event template
    return render_template('events/save_event.html', form=form)


@events.route("/show_events")
def show_events():
    """
    Displays all saved events
    """
    all_events = get_all_events()
    return render_template("events/show_events.html", events=all_events)


@events.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    """
    Edit an Event
    """
    event = get_event(event_id)
    form = SaveEventForm(obj=event)
    if form.validate_on_submit():
        # If there is a change in values in the timestamp, event subject or event content,
        # revoke current task and send new updated email.
        if event.timestamp != form.timestamp.data or event.event_subject != form.event_subject.data or \
                event.event_content != form.event_content.data:

            # Revoke task
            tasks = get_task_id_for_event(event_id)
            for task in tasks:
                revoke_task(task.task_id)

            # Update changes
            event.event_id = form.event_id.data
            event.event_subject = form.event_subject.data
            event.event_content = form.event_content.data
            event.timestamp = form.timestamp.data
            db.session.commit()

            # Resend emails with updated values
            resend_emails = get_all_email_for_event(event_id)
            for recipient_data in resend_emails:
                send_email(form.event_id.data, recipient_data.email, recipient_data.id)
            flash('You have successfully edited the event.')

            # redirect to the events page
            return redirect(url_for('events.show_events'))

    form.event_id.data = event.event_id
    form.event_subject.data = event.event_subject
    form.event_content.data = event.event_content
    form.timestamp.data = event.timestamp

    return render_template('events/edit_event.html', action='Edit', form=form, event=event)


@events.route('/delete_events/<int:event_id>', methods=['GET', 'POST'])
def delete_event(event_id):
    """
    Delete an Event
    """
    event = get_event(event_id)
    # Get all the recipients that are associated with the deleted event
    recipients = get_all_recipient_for_event(event_id)

    # Remove all associated participants from database
    for recipient in recipients:
        db.session.delete(get_recipient(recipient))

    # Remove deleted event from database
    db.session.delete(event)

    # Revoke all task associated with the deleted event from data
    tasks = get_task_id_for_event(event_id)
    for task in tasks:
        revoke_task(task.task_id)

    # Commit
    db.session.commit()

    flash('You have successfully deleted the event')

    # redirect to the show events page
    return redirect(url_for('events.show_events'))

