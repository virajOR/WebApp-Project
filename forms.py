from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class MeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    meeting_date = DateField('Meeting Date', format='%Y-%m-%d', validators=[DataRequired()])
    meeting_time = TimeField('Meeting Time', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Create Meeting')

class TaskForm(FlaskForm):
    name = StringField('Task Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])  # Add this line
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    due_time = TimeField('Due Time', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Create Task')