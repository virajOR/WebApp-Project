from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import MeetingForm, TaskForm
from models import db, Meeting, Task
from task_predictor import predict_delayed_tasks, predict_delayed_meetings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db.init_app(app)

def recreate_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database tables recreated successfully.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/meetings', methods=['GET', 'POST'])
def manage_meetings():
    form = MeetingForm()
    if form.validate_on_submit():
        meeting_datetime = datetime.combine(form.meeting_date.data, form.meeting_time.data)
        new_meeting = Meeting(
            title=form.title.data,
            description=form.description.data,
            meeting_date=meeting_datetime,
        )
        db.session.add(new_meeting)
        db.session.commit()
        return redirect(url_for('manage_meetings'))

    meetings = Meeting.query.all()
    delayed_meetings = predict_delayed_meetings(meetings)
    
    return render_template('meetings.html', meetings=meetings, delayed_meetings=delayed_meetings, form=form)

@app.route("/delete_meetings/<int:id>")
def delete_meetings(id):
    meeting = Meeting.query.filter_by(id=id).first()
    db.session.delete(meeting);
    db.session.commit()
    return redirect("/meetings")

@app.route("/delete_tasks/<int:id>")
def delete_tasks(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task);
    db.session.commit()
    return redirect("/tasks")

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    form = TaskForm()
    if form.validate_on_submit():
        due_datetime = datetime.combine(form.due_date.data, form.due_time.data)
        new_task = Task(
            name=form.name.data,
            description=form.description.data,
            due_date=due_datetime
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('manage_tasks'))

    tasks = Task.query.all()
    delayed_tasks = predict_delayed_tasks(tasks)
    return render_template('tasks.html', form=form, tasks=tasks, delayed_tasks=delayed_tasks)


@app.route("/about", methods = ['GET', 'POST'])
def about_app():
    return render_template('about.html')

if __name__ == '__main__':
    recreate_db()  
    app.run(debug=True)