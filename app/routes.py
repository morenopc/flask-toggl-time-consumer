from sqlalchemy import desc
from flask import redirect, url_for, request, render_template
from app import app
from app import db
from app.toggl_api import toggl_api
from app.models import Client, Project, Task


@app.route('/toggl-api')
def get_toggl_task():
    toggl_api()
    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
def index():

    entries = db.session.query(
        Task, Project, Client).order_by(
            desc(Task.start)).order_by(     # month (descending)
            desc(Task.duration)).order_by(  # task time (descending)
            Project.name                    # project name (alphabetically)
    ).join(Project).join(Client).all()

    return render_template(
        'index.html', title='Time Consuming Tasks', entries=entries)


@app.route('/time-consuming')
def time_consuming_form():

    hours = request.args.get('hours') or 1
    millisec = int(hours) * 1000 * 60 * 60  # hours to miliseconds

    entries = db.session.query(
        Task, Project, Client).order_by(
            desc(Task.start)).order_by(     # month (descending)
            desc(Task.duration)).order_by(  # task time (descending)
            Project.name                    # project name (alphabetically)
    ).filter(Task.duration >= millisec).join(Project).join(Client).all()

    return render_template(
        'index.html', title='Time Consuming Tasks', entries=entries, value=hours)
