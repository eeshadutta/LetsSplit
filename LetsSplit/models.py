from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class users(DB.Model):
    __searchable__ = ['name']
    id = DB.Column('user_id', DB.Integer, primary_key = True)
    email = DB.Column(DB.String(100))
    username = DB.Column(DB.String(50))
    password = DB.Column(DB.String(200))
    DOB = DB.Column(DB.String(10))
    profile_pic = DB.Column(DB.String(100))
    name = DB.Column(DB.String(100))
    bio = DB.Column(DB.String(200))

    def __init__(self, email, username, password, DOB ,profile_pic_url, name, bio):
        self.email = email
        self.username = username
        self.password = password
        self.DOB = DOB
        self.profile_pic = profile_pic_url
        self.name = name
        self.bio = bio

class friends(DB.Model):
    id = DB.Column('user_id', DB.Integer, primary_key = True)
    username = DB.Column(DB.String(50))
    friend = DB.Column(DB.String(8000))
    
    def __init__(self, username, friends=''):
        self.username = username
        self.friend = ''
        

class transactions(DB.Model):
    id = DB.Column('user_id', DB.Integer, primary_key=True)
    from_user = DB.Column(DB.String(50))
    to_user = DB.Column(DB.String(50))
    amount = DB.Column(DB.String(10))
    settled = DB.Column(DB.String(1))
    date_created = DB.Column(DB.String(50))
    date_settled = DB.Column(DB.String(50))
    comments = DB.Column(DB.String(10000))

    def __init__(self, from_user, to_user, amount, settled, date_created, date_settled=''):
        self.from_user = from_user
        self.to_user = to_user
        self.amount = amount
        self.settled = settled
        self.date_created = date_created
        self.date_settled = date_settled
        self.comments = ''


class groups(DB.Model):
    id = DB.Column('user_id', DB.Integer, primary_key=True)
    group_name = DB.Column(DB.String(50))
    group_members = DB.Column(DB.String(5000))

    def __init__(self, name, group_members):
        self.group_name = name
        self.group_members = group_members
