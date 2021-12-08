# ORM 방식으로 데이터베이스에 객체를 통해 접근 (SQL 질의어 없이도 데이터베이스 접근 가능)
# 아래의 코드에서 각 클래스의 이름은 DB의 테이블과 매핑하여 사용한다.

# created by 장지욱 11.09 
# modified by 장지욱 11.16 - User, Post 클래스 구현
#                   11.25 - Seat, Reservation 클래스 구현

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
    distance = db.Column(db.Integer, default = 0)
    acheater = db.Column(db.Integer, default = 0)
    windownear = db.Column(db.Integer, default = 0)
    door = db.Column(db.Integer, default = 0)

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

class Seat(db.Model):
     __tablename__ = 'seat'
     seatNum = db.Column(db.Integer,  primary_key=True,
                    nullable=False, autoincrement=True)
     user_id = db.Column(db.String(30), nullable = False)
     used = db.Column(db.Integer, default = '0')
     finish_time = db.Column(db.DateTime, default= 0)

     def __init__(self,seatNum,user_id,used,finish_time):
         self.seatNum = seatNum
         self.user_id = user_id
         self.used = used
         self.finish_time = finish_time

class Reservation(db.Model):
     __tablename__ = 'reservation'
     reservationID = db.Column(db.Integer,  primary_key=True,
                    nullable=False, autoincrement=True)
     seatNum = db.Column(db.Integer, nullable=False)
     user_id = db.Column(db.String(255), nullable=False)
     reserved_time = db.Column(db.DateTime, default=datetime.utcnow)
     starttime = db.Column(db.DateTime, default=datetime.utcnow)
     finishtime = db.Column(db.DateTime, default=datetime.utcnow)

     def __init__(self,seatNum,user_id,reserved_time,starttime,finishtime):
         self.seatNum = seatNum
         self.user_id = user_id
         self.reserved_time = reserved_time
         self.starttime = starttime
         self.finishtime = finishtime

# 아래는 테이블 작성했던 sql문입니다. 추후 수정사항이 생길 수도 있습니다. - 장지욱
# create table User (
#     studentID INT NOT NULL AUTO_INCREMENT,
#     username char(10) NOT NULL,
#     user_id char(20) NOT NULL UNIQUE,
#     user_pw char(100) NOT NULL,
#     userphone char(30) NOT NULL,
#     useremail char(50) NOT NULL,
#     distance INT,
#     acheater INT,
#     windownear INT,
#     door INT,
#     PRIMARY KEY(studentID));

# create table Post (
#     id INT NOT NULL AUTO_INCREMENT,
#     author char(50) not null,
#     content TEXT,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY(id));

# create table Reservation (
#     reservationID INT NOT NULL AUTO_INCREMENT,
#     seatNum INT NOT NULL,
#     user_id VARCHAR(30) NOT NULL,
#     reserved_time DATETIME DEFAULT CURRENT_TIMESTAMP,
#     starttime DATETIME DEFAULT CURRENT_TIMESTAMP,
#     finishtime DATETIME DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY(reservationID));

# create table Seat (
#     seatNum INT NOT NULL AUTO_INCREMENT,
#     user_id VARCHAR(30),
#     used INT DEFAULT '0',
#     finish_time DATETIME DEFAULT NULL,
#     PRIMARY KEY(seatNum));