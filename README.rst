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

    (venv) $ export FLASK_APP=task.py
    (venv) $ flask run

Open http://127.0.0.1:5000 in a browser.


Database Migration
------------------

::

    (venv) $ export FLASK_APP=task.py
    (venv) $ flask db migrate
    (venv) $ flask db upgrade
