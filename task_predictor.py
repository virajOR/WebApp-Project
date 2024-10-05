from datetime import datetime, timedelta

def predict_delayed_tasks(tasks):
    delayed_tasks = []
    now = datetime.utcnow()
    
    for task in tasks:
       if now <=task.due_date <= (now + timedelta(minutes=24)):
            delayed_tasks.append(task)
    return delayed_tasks

def predict_delayed_meetings(meetings):
    delayed_meetings = []
    wrong_time = []
    now = datetime.utcnow()
    print(f"Current time: {now}")
    
    for meeting in meetings:
        if now <= meeting.meeting_date <= (now + timedelta(minutes=30)):
            delayed_meetings.append(meeting)
    return delayed_meetings