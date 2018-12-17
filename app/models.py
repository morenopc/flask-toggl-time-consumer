from app import db
from datetime import datetime


members = db.Table(
    'members',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)


class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Workspace {}>'.format(self.name)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), default='(No Client)')

    def __repr__(self):
        return '<Client {}>'.format(self.name)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<Member {}>'.format(self.name)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    status = db.Column(db.Integer, default=0)
    members = db.relationship('Member', secondary=members, lazy='dynamic',
                              backref=db.backref('projects', lazy=True))

    def __repr__(self):
        return '<Project {}>'.format(self.name)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end = db.Column(db.DateTime)
    duration = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task {} {}>'.format(self.name, self.start, self.end)
