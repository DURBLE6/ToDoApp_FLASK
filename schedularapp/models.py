from datetime import datetime
from email.policy import default
from . import db

class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key = True, autoincrement = True, nullable = True)
    firstname = db.Column(db.String(100), nullable = True)
    lastname = db.Column(db.String(100), nullable = True)
    email = db.Column(db.String(100), nullable = True)
    password = db.Column(db.String(150), nullable = True)


class Task(db.Model):
    task_id = db.Column(db.Integer(), primary_key = True, autoincrement = True, nullable = True)
    title = db.Column(db.String(100), nullable = True)
    notes = db.Column(db.String(100), nullable = True)
    date = db.Column(db.Date(), default=datetime.utcnow())
    status = db.Column(db.Enum('1','0'), server_default = ('0'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable = False)
