from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired


class SaveEventForm(FlaskForm):
    """
    Form to create a new event
    """
    event_id = IntegerField('Event Id', validators=[DataRequired(message='Please enter event ID')],
                            render_kw={"placeholder": "Enter Event ID"})
    event_subject = StringField('Event Subject', validators=[DataRequired(message='Please enter event subject')],
                                render_kw={"placeholder": "Enter Event Subject"})
    event_content = TextAreaField('Event Content', validators=[DataRequired(message='Please enter event content')],
                                render_kw={"placeholder": "Enter Event Content", "rows": 5, "cols": 11})
    timestamp = DateTimeField('Date & Time', format='%d %b %Y %H:%M',
                              validators=[DataRequired(message='Please select a date and time')],
                              render_kw={"placeholder": "Enter select Date and Time"})
    submit = SubmitField()
