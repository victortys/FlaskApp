from flask import flash, redirect, render_template, url_for

from . import recipients
from forms import SaveRecipientForm
from app import db
from ..email import send_email, revoke_task
from ..models import Recipient, get_all_recipients, get_recipient, get_all_events, get_task_id


@recipients.route('/save_recipient', methods=['GET', 'POST'])
def save_recipient():
    """"
    Add a recipient to the database
    """
    event_names = get_all_events()

    # Populate the Select List with Event names
    event_list = [(i.event_id, i.event_subject) for i in event_names]
    form = SaveRecipientForm()
    form.event_id.choices = event_list

    if form.validate_on_submit():
        recipient = Recipient(name=form.recipient_name.data,
                              email=form.recipient_email.data,
                              event_id=form.event_id.data)

        # add new recipient to database
        db.session.add(recipient)
        db.session.flush()
        recipient_id = recipient.id
        db.session.commit()
        flash('You have successfully save a new recipient!')
        send_email(form.event_id.data, form.recipient_email.data, recipient_id)

        # redirect to home page
        return redirect(url_for('recipients.show_recipients'))

    # load save event template
    return render_template('recipients/save_recipient.html', form=form)


@recipients.route("/show_recipients")
def show_recipients():
    """
    Display all recipient
    """
    all_recipients = get_all_recipients()
    return render_template("recipients/show_recipients.html", recipients=all_recipients)


@recipients.route('/edit_recipient/<int:recipient_id>', methods=['GET', 'POST'])
def edit_recipient(recipient_id):
    """
    Edit a recipient
    """
    recipient = get_recipient(recipient_id)
    event_names = get_all_events()

    # Populate the Select List with Event names
    event_list = [(i.event_id, i.event_subject) for i in event_names]
    form = SaveRecipientForm(obj=recipient)
    form.event_id.choices = event_list

    if form.validate_on_submit():
        recipient.name = form.recipient_name.data
        recipient.email = form.recipient_email.data

        # If there is a change in event, the previous task will be revoked
        if recipient.event_id != form.event_id.data:
            revoke_task(get_task_id(recipient_id).task_id)
            send_email(form.event_id.data, form.recipient_email.data, recipient_id)

        recipient.event_id = form.event_id.data

        db.session.commit()
        flash('You have successfully edited the recipient.')

        # redirect to the events page
        return redirect(url_for('recipients.show_recipients'))
    
    form.recipient_name.data = recipient.name
    form.recipient_email.data = recipient.email
    form.event_id.data = recipient.event_id

    return render_template('recipients/edit_recipient.html', action='Edit', form=form, recipient=recipient)


@recipients.route('/delete_recipient/<int:recipient_id>', methods=['GET', 'POST'])
def delete_recipient(recipient_id):
    """
    Delete a recipient
    """
    recipient = get_recipient(recipient_id)

    db.session.delete(recipient)
    db.session.commit()
    flash('You have successfully deleted the recipient')

    # redirect to the show recipients page
    return redirect(url_for('recipients.show_recipients'))


