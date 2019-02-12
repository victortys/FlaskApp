from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email


class SaveRecipientForm(FlaskForm):
    """
    Form to create a new recipient
    """
    recipient_name = StringField('Name', validators=[DataRequired(message='Please enter recipient name')],
                                 render_kw={"placeholder": "Enter recipient name"})
    recipient_email = StringField('Email', validators=[DataRequired(message='Please enter recipient email'), Email()],
                                  render_kw={"placeholder": "Enter recipient email"})
    event_id = SelectField('Event', coerce=int)
    submit = SubmitField('Save')
