import os
import urllib
import datetime
from toggl.TogglPy import Toggl

from app import db
from app.models import Workspace, Client, Member, Project, Task

toggl = Toggl()
TOGGL_API_KEY = os.environ.get('TOGGL_API_KEY')
toggl.setAPIKey(TOGGL_API_KEY)

DEFAULT_LONG_TASK = 3600000  # 1 hour
WORKSPACE_ID = 3122278
workspace = Workspace.query.filter_by(name='Vitamin').first()
if workspace is None:
    workspace = Workspace(id=WORKSPACE_ID, name='Vitamin')
    db.session.add(workspace)
    db.session.commit()

USER_AGENT = 'api_test'
REPORTS_URL = 'https://toggl.com/reports/api/v2/'
WORKSPACES_URL = 'https://www.toggl.com/api/v8/workspaces/'
PROJECTS_URL = 'https://www.toggl.com/api/v8/projects/'
PARAMET_URL = urllib.parse.urlencode({
    'workspace_id': workspace.id,
    'since': '2018-09-01T00:00:00Z',  # Sep 2018
    'until': '2018-10-31T00:00:00Z',  # Out 2010
    'user_agent': USER_AGENT,
})


def toggl_api(duration=None):
    # GET all Workspace members
    users = toggl.request(''.join([WORKSPACES_URL, str(workspace.id), '/users']))
    for user in users:
        member = Member.query.filter_by(id=user.get('id')).first()
        if member is None:
            member = Member(
                id=user.get('id'), name=user.get('fullname'), email=user.get('email'))
            db.session.add(member)
        db.session.commit()

    # GET Detailed report time entries
    response = toggl.request(''.join([REPORTS_URL, 'details?', PARAMET_URL]))
    for data in response.get('data'):

        client = Client.query.filter_by(name=data.get('client')).first()
        if client is None:
            client = Client(name=data.get('client') or '(no client)')
            db.session.add(client)

        member = Member.query.filter_by(id=data.get('uid')).first()
        if member is None:
            member = Member(id=data.get('uid'), name=data.get('user'))
            db.session.add(member)

        project = Project.query.filter_by(id=data.get('pid')).first()
        if project is None:

            project = Project(
                name=data.get('project') or '(without a project)',
                workspace_id=workspace.id,
                client_id=client.id)

            if data.get('pid') is not None:
                project.id = data.get('pid')

                # GET all Project members
                project_users = toggl.request(''.join(
                    [PROJECTS_URL, str(data.get('pid')), '/project_users']))
                for user in project_users:
                    member = Member.query.filter_by(id=user.get('uid')).first()
                    project.members.append(member)

            db.session.add(project)
            db.session.commit()

        if data.get('dur') > DEFAULT_LONG_TASK:
            task = Task.query.filter_by(id=data.get('id')).first()
            if task is None:
                task = Task(
                    id=data.get('id'),
                    name=data.get('description') or '(no description)',
                    project_id=project.id,
                    start=datetime.datetime.fromisoformat(data.get('start')),
                    end=datetime.datetime.fromisoformat(data.get('end')),
                    duration=data.get('dur'))
                db.session.add(task)

    db.session.commit()
