Time Consumer Tasks
===================

Since time-consumers tasks are an indication of a problem with that task, we want to have a
tool that allows to easily identify them.


Install
-------

::

    # clone the repository
    git clone https://github.com/morenopc/flask-toggl-time-consumer
    cd flask-toggl-time-consumer

Create a virtualenv and activate it::

    python3 -m venv venv
    . venv/bin/activate

Install requirements::

    # just in case, update pip
    (venv) $ pip install -U pip
    (venv) $ pip install -r requirements


Run
---

::
    # TOGGL API TOKEN
    (venv) $ export TOGGL_API_KEY=<your toggl API key>
    (venv) $ export FLASK_APP=task.py
    (venv) $ flask run

Open http://127.0.0.1:5000 in a browser.


Database Migration
------------------

::

    (venv) $ export FLASK_APP=task.py
    (venv) $ flask db migrate
    (venv) $ flask db upgrade


Cron
----

::

    # cron task to run each 15 minute
    0,15,30,45 * * * * <path to> run_toggl_api.sh
