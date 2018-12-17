from flask import render_template
from app import app
from app.toggl_api import toggl_api


@app.route('/toggl-api')
def get_toggl_task():
    toggl_api()
    return 'Done!'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Time Consumer Tasks')
