# backend api를 구현한 파일로, 각 필요한 함수들(로그인, 회원가입, 게시판/수정/삭제, 좌석예약) 정의

# created by 장지욱 11.09
# modified by 장지욱 11.14 - 회원가입, 로그인 구현, 세션 관리 구현
#                   11.20 - 게시판 확인/post/수정/삭제 구현, 아이디 중복 방지 기능 추가
#                   11.23 - 본인 예약내역 전달 구현/ 다가올 내역만 전달 기능 구현
#                   11.24 - 예약 기능/수정/삭제 초안 구현
#                   11.25 - 예약 중복 방지 기능 추가
#                   11.28 - 예약 중복 방지 기능 수정 및 예약시 발생할 수 있는 오류사랑 방지 기능 추가

from re import S
from flask import json, redirect, request, render_template, jsonify, Blueprint, session, g
from models import User, Post, Reservation
# Seat
from db_connect import db
from flask_bcrypt import Bcrypt
from datetime import date, datetime, timedelta

board = Blueprint('board',__name__)
bcrypt = Bcrypt()

# 세션관리
@board.before_app_request
def load_logged_in_user(): #이미 로그인을 한 경우, 그 로그인 정보를 세션으로 남겨, 다시 접속하더라도 귀찮게 로그인을 다시 하지 않아도 된다.
    user_id = session.get('login')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.user_id == user_id).first()

@board.route("/")
def home(): 
    if session.get('login') is None:
        return redirect("/login")
    else:
        return redirect("/main")

# 회원가입
@board.route("/join",methods=["GET","POST"])
def join(): #회원가입 정보를 Front에서 받아, 정보들을 DB에 저장한다. 리턴값: json 형식으로 성공,실패 여부를 Front에 전달한다.
    if session.get("login") is None:
        if request.method == 'GET':
            return render_template('join.html')
        else:
            user_idcheck = db.session.query(User.user_id).all()
            user_idcheck = [x[0] for x in user_idcheck]

            user_id = request.form['user_id']

            if user_id in user_idcheck: #아이디 중복 여부 체크하고, 이미 아이디가 있으면 json형식으로 아이디있음을 전달
                return jsonify({"result":"alreadyID"})

            user_pw = request.form['user_pw']
            pw_hash = bcrypt.generate_password_hash(user_pw)
            username = request.form['username']
            userphone = request.form['userphone']
            useremail = request.form['useremail']
            distance = request.form['distance']
            acheater = request.form['acheater']
            windownear = request.form['windownear']
            door = request.form['door']

            user = User(username,user_id,pw_hash,userphone,useremail,distance,acheater,windownear,door)
                
            db.session.add(user)
            db.session.commit()
            return jsonify({"result":"success"})
    else:
        return redirect("/")

# 로그인
@board.route("/login", methods=['GET','POST'])
def login(): #로그인 정보를 입력받고, DB와의 로그인 정보 일치 여부를 확인하고 그거에 대한 return값으로 성공 실패여부를 json 형식으로 전달한다.
    if session.get("login") is None:
        if request.method == 'GET':
            return render_template('login.html')
        else:
            user_id = request.form['user_id']
            user_pw = request.form['user_pw']
            user = User.query.filter(User.user_id == user_id).first()
            if user is not None:
                if bcrypt.check_password_hash(user.user_pw, user_pw):
                    session['login'] = user.user_id
                    return jsonify({"result": "success"})
                else:
                    return jsonify({"result": "fail"})
            else:
                return jsonify({"result": "fail"})
    else:
        return redirect("/")

# 로그아웃
@board.route("/logout")
def logout(): #로그아웃 기능을 구현하는데, 세션값을 none으로 만들어준다.
    session['login'] = None
    return redirect('/')

# 게시글 작성
@board.route("/post", methods=["GET","POST"])
def post(): #request.method가 get일 경우, 게시물을 올라온 순서로 보여주고, request.method가 post일 경우, 내용과 작성자를 입력받고, 그 내용을 DB에 저장한다.
    if session.get("login") is not None:
        if request.method == 'GET':
            data = Post.query.order_by(Post.created_at.desc()).all()
            return render_template("post.html", post_list = data)
        else:
            content = request.form['content']
            author = request.form['author']

            post = Post(author,content)
            db.session.add(post)
            db.session.commit()
            return jsonify({"result":"success"})
    else:
        return redirect("/")

# 게시글 삭제
@board.route("/post", methods=["DELETE"])
def delete_post(): #본인의 post내용을 삭제할 수 있게 하고, DB에서도 삭제를 한다.
    id = request.form['id']
    author = request.form['author']
    data = Post.query.filter(Post.id == id, Post.author == author).first()
    if data is not None:
        db.session.delete(data)
        db.session.commit()
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail'})

# 게시글 수정
@board.route("/post", methods=["PATCH"])
def update_post(): #본인의 post내용을 수정할 수 있게 하고, DB에도 그 수정사항을 반영한다.
    id = request.form['id']
    content = request.form['content']
    author = User.query.filter(User.user_id == session['login']).first()

    data = Post.query.filter(
        Post.id == id, Post.author == author.user_id
    ).first()

    data.content = content
    db.session.commit()

    return jsonify({'result': 'success'})

# 예약 내역 
@board.route('/main')
def show_myreserve(): #본인의 다가올 예약내역을 리스트 형태로 전달한다. 리턴값:reserve_list
    if session.get("login") is not None: 
        if request.method == 'GET':
            new_data = []
            data = Reservation.query.filter(Reservation.user_id == session['login']).all()
            now = datetime.now()
            for i in range(len(data)):
                if data[i].finishtime > now:
                    new_data.append(data[i]) 
            return render_template("main.html", reserve_list = new_data)
    else:
        return redirect("/")


# 예약 기능 구현 (test x)
@board.route('/reserve', methods=['GET','POST'])
def reserve():
    if session.get("login") is not None:
        if request.method == 'GET':
            #좌석 추천 알고리즘을 여기다 넣어도 될거같기도...
            return render_template('reserve.html')
        else:
            now = datetime.now()
            seatNum = request.form['seatNum']
            user_id = request.form['user_id']
            reserved_time = request.form['reserved_time']
            starttime = request.form['starttime']
            finishtime = request.form['finishtime']

            #사용 시간은 무조건 지금보다는 앞에 해야한다.
            if starttime > now: 
                return jsonify({"result":"NoReserve"}) # 사용시간이 지금 시각보다 늦은경우

            #끝나는 시간이 시작시간보다 더 앞이면 알람경고
            if starttime > finishtime: 
                return jsonify({"result":"starttimeFirst"}) 

            #하루이상 넘어가는 예약은 불가능하다..
            if starttime.day != finishtime.day:
                return jsonify({"result":"OnedayOnly"})

            #유저가 다른 좌석을 그 당일 이미 예약했으면 다른 자리 불가 TwoReserveImpossibleAtSameDay
            user_timecheck = Reservation.query.filter(Reservation.user_id==user_id).all()
            for i in range(len(user_timecheck)):
                if user_timecheck[i].starttime.day == starttime.day:
                    return jsonify({"result":"TwoReserveImpossibleAtSameDay"})

            # 좌석예약하려는 시간에 예약이 있는 경우 AlreadySeat json형태로 보냄
            reserve_data = Reservation.query.filter(Reservation.seatNum == seatNum, Reservation.starttime >= now).all()
            for i in range(len(reserve_data)):
                if (starttime < reserve_data[i].starttime < finishtime) or (starttime < reserve_data[i].finishtime < finishtime) or (starttime<reserve_data[i].starttime and finishtime>reserved_time[i].finishtime):
                    return jsonify({"result":"AlreadySeat"})

            reserve = Reservation(seatNum,user_id,reserved_time,starttime,finishtime)
            db.session.add(reserve)
            db.session.commit()
            return jsonify({"result":"success"})
    else:
        return redirect("/")

# # 예약 수정 (test x)
# @board.route("/reserve", methods=["PATCH"])
# def update_reserve(): #본인의 예약내용을 수정할 수 있게 하고, DB에도 그 수정사항을 반영한다.
#     now = datetime.now()
#     reservationID = request.form['reservationID']
#     seatNum = request.form['seatNum']
#     user_id = request.form['user_id']
#     reserved_time = request.form['reserved_time']
#     starttime = request.form['starttime']
#     finishtime = request.form['finishtime']

#     #사용 시간은 무조건 지금보다는 앞에 해야한다.
#     if starttime > now: 
#         return jsonify({"result":"NoReserve"}) # 사용시간이 지금 시각보다 늦은경우

#     #끝나는 시간이 시작시간보다 더 앞이면 알람경고
#     if starttime > finishtime: 
#         return jsonify({"result":"starttimeFirst"}) 

#     #유저가 다른 좌석을 그 당일 이미 예약했으면 다른 자리 불가 TwoReserveImpossibleAtSameDay
#     user_timecheck = Reservation.query.filter(Reservation.user_id==user_id).all()
#     for i in range(len(user_timecheck)):
#         if user_timecheck[i].starttime.day == starttime.day:
#             return jsonify({"result":"TwoReserveImpossibleAtSameDay"})

#     # 좌석예약하려는 시간에 예약이 있는 경우 AlreadySeat json형태로 보냄
#     reserve_data = Reservation.query.filter(Reservation.seatNum == seatNum, Reservation.starttime >= now).all()
#     for i in range(len(reserve_data)):
#         if (starttime < reserve_data[i].starttime < finishtime) or (starttime < reserve_data[i].finishtime < finishtime) or (starttime<reserve_data[i].starttime and finishtime>reserved_time[i].finishtime):
#             return jsonify("result":"AlreadySeat")

#     data = Reservation.query.filter(Reservation.reservationID == reservationID, Reservation.user_id == user_id).first()
#     data.seatNum = seatNum
#     data.reserved_time = reserved_time
#     data.starttime = starttime
#     data.finishtime = finishtime
#     db.session.commit()

#     return jsonify({"result":"success"})

# # 예약 삭제 (test x)
# @board.route("/reserve", methods=["DELETE"])
# def delete_reserve(): #본인의 예약내용을 삭제할 수 있게 하고, DB에도 삭제한다.
#     reservationID = request.form['reservationID']
#     seatNum = request.form['seatNum']
#     user_id = request.form['user_id']
#     reserve_data = Reservation.query.filter(Reservation.reservationID == reservationID, Reservation.seatNum == seatNum, Reservation.user_id == user_id).first()
#     if reserve_data is not None:
#         db.session.delete(reserve_data)
#         db.session.commit()
#         return jsonify({'result':'success'})
#     else:
#         return jsonify({'result':'fail'})


