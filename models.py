# DB와 연동해주는 파일

# created by 장지욱 11.09

from sqlalchemy.sql.schema import ForeignKey
from db_connect import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    studentID = db.Column(db.Integer,  primary_key=True,
                   nullable=False, autoincrement=True)
    username = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.String(20), nullable=False, unique=True)
    user_pw = db.Column(db.String(100), nullable=False)
    userphone = db.Column(db.String(30), nullable=False)
    useremail = db.Column(db.String(50))
    distance = db.Column(db.Integer, default = '0')
    acheater = db.Column(db.Integer, default = '0')
    windownear = db.Column(db.Integer, default = '0')
    door = db.Column(db.Integer, default = '0')

    def __init__(self,username,user_id,user_pw,userphone,useremail,distance,acheater,windownear,door):
        self.username = username
        self.user_id = user_id
        self.user_pw = user_pw
        self.userphone = userphone
        self.useremail = useremail
        self.distance = distance
        self.acheater = acheater
        self.windownear = windownear
        self.door = door

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,  primary_key=True,
                   nullable=False, autoincrement=True)
    author = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, author,content):
        self.author = author
        self.content = content