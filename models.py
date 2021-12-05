# ORM 방식으로 데이터베이스에 객체를 통해 접근 (SQL 질의어 없이도 데이터베이스 접근 가능)
# 아래의 코드에서 각 클래스의 이름은 DB의 테이블과 매핑하여 사용한다.

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
    # distance = db.Column(db.Integer, default = '0')
    # acheater = db.Column(db.Integer, default = '0')
    # windownear = db.Column(db.Integer, default = '0')
    # door = db.Column(db.Integer, default = '0')

    def __init__(self,username,user_id,user_pw,userphone,useremail):
    # ,distance,acheater,windownear,door):
        self.username = username
        self.user_id = user_id
        self.user_pw = user_pw
        self.userphone = userphone
        self.useremail = useremail
        # self.distance = distance
        # self.acheater = acheater
        # self.windownear = windownear
        # self.door = door

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

# class Seat(db.Model):
#     __tablename__ = 'seat'
#     seatNum = db.Column(db.Integer,  primary_key=True,
#                    nullable=False, autoincrement=True)
#     studentID = db.Column(db.Integer, ForeignKey(User.studentID))
#     used = db.Column(db.Integer, default = '0')
#     finish_time = db.Column(db.DateTime, default=datetime.utcnow)

#     def __init__(self,studentID,used):
#         self.studentID = studentID
#         self.used = used

# class Reservation(db.Model):
#     __tablename__ = 'reseration'
#     reservationID = db.Column(db.Integer,  primary_key=True,
#                    nullable=False, autoincrement=True)
#     seatNum = db.Column(db.Integer, ForeignKey(Seat.seatNum), nullable=False)
#     studentID = db.Column(db.String(255), nullable=False)
#     reserved_time = db.Column(db.DateTime, default=datetime.utcnow)
#     starttime = db.Column(db.DateTime, default=datetime.utcnow)
#     finishtime = db.Column(db.DateTime, default=datetime.utcnow)

#     def __init__(self,seatNum,studentID,reserved_time,starttime,finishtime):
#         self.seatNum = seatNum
#         self.studentID = studentID
#         self.reserved_time = reserved_time
#         self.starttime = starttime
#         self.finishtime = finishtime
    