# backend api를 구현한 파일로, 각 필요한 함수들(로그인, 회원가입, 게시판/수정/삭제, 좌석예약) 정의

# created by 장지욱 11.09
# modified by 장지욱 11.14 - 회원가입, 로그인 구현, 세션 관리 구현
#                   11.20 - 게시판 확인/post/수정/삭제 구현, 아이디 중복 방지 기능 추가
#                   11.23 - 본인 예약내역 전달 구현/ 다가올 내역만 전달 기능 구현
#                   11.24 - 예약 기능/수정/삭제 초안 구현
#                   11.25 - 예약 중복 방지 기능 추가
#                   11.28 - 예약 중복 방지 기능 수정 및 예약시 발생할 수 있는 오류사랑 방지 기능 추가
#                   12.04 - 좌석 실시간 정보 업데이트하기 Reservation 테이블에서 시작시간, 종료시간에 맞춰서 Seat 테이블 정보 변경해주기

import re
from flask import json, redirect, request, render_template, jsonify, Blueprint, session, g
from models import User, Post, Reservation, Seat
from db_connect import db
from flask_bcrypt import Bcrypt
from datetime import datetime

board = Blueprint('board',__name__)
bcrypt = Bcrypt()
g
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
            windowfar = request.form['windowfar']
            door = request.form['door']

            user = User(username,user_id,pw_hash,userphone,useremail,distance,acheater,windowfar,door)
                
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

# 예약 기능 구현
@board.route('/reserve', methods=['GET','POST'])
def reserve():
    if session.get("login") is not None:
        if request.method == 'GET':
            data = Seat.query.filter(Seat.used == 1).all() #지금 사용중인 좌석 정보
            preference_info = db.session.query(User.distance,User.acheater,User.windowfar,User.door).filter(User.user_id == session['login']).first()
            preference_seat = recommend(preference_info[0],preference_info[1],preference_info[2],preference_info[3])
            data.append(preference_seat)
            return render_template('reserve.html', seat_list = data) # seat_list 현재 좌석 정보 넘겨주기 + seat_list[-1]에 알고리즘을 통한 추천좌석까지 보내줌
        else:
            now = datetime.now()
            seatNum = request.form['seatNum']
            user_id = request.form['user_id']
            reserved_time = now
            starttime = datetime.strptime(request.form['starttime'], '%Y/%m/%d %H:%M')
            finishtime = datetime.strptime(request.form['finishtime'], '%Y/%m/%d %H:%M')

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
                if ((starttime <= reserve_data[i].starttime <= finishtime) or (starttime <= reserve_data[i].finishtime <= finishtime) or (starttime<=reserve_data[i].starttime and finishtime>=reserve_data[i].finishtime) or (starttime>=reserve_data[i].starttime and finishtime<=reserve_data[i].finishtime)):
                    return jsonify({"result":"AlreadySeat"})

            reserve = Reservation(seatNum,user_id,reserved_time,starttime,finishtime)
            db.session.add(reserve)
            db.session.commit()
            return jsonify({"result":"success"})
    else:
        return redirect("/")

# 예약 삭제 
@board.route("/main", methods=["DELETE"])
def delete_reserve(): #본인의 예약내용을 삭제할 수 있게 하고, DB에도 삭제한다. 
    if session.get("login") is not None:
        reservationID = request.form['reservationID']
        seatNum = request.form['seatNum']
        user_id = request.form['user_id']
        reserve_data = Reservation.query.filter(Reservation.reservationID == reservationID, Reservation.seatNum == seatNum, Reservation.user_id == user_id).first()
        seat_data = Seat.query.filter(Seat.seatNum == seatNum, Seat.used == 1, Reservation.user_id == Seat.user_id).first()
        if reserve_data is not None:
            db.session.delete(reserve_data)
            db.session.commit()
            if seat_data is not None:
                user_id = None
                used = 0
                finish_time = None

                seat_data.user_id = user_id
                seat_data.used = used
                seat_data.finish_time = finish_time
                db.session.commit()
            
            return jsonify({'result':'success'})
        else:
            return jsonify({'result':'fail'})

# 좌석 초기화 -> 매 오후 12시에 좌석 table을 초기화해주기
def seat_initialize():
    seatinfo = db.session.query(Seat).all()
    for i in range(len(seatinfo)):
        seatinfo[i].user_id = None
        seatinfo[i].used = 0
        seatinfo[i].finish_time = None
        db.session.commit()

# 좌석 정보 업데이트하기 Reservation 테이블에서 시작시간에 맞춰서 Seat 테이블 정보 변경해주기
def seat_update():
    now = datetime.now()
    temp_time = now.strftime('%Y-%m-%d %H:%M')
    now = datetime.strptime(temp_time,'%Y-%m-%d %H:%M')
    
    # 유저가 사용시작시간이 되어 Seat 테이블을 최신화해주는 경우
    seatInfoinput = db.session.query(Reservation.user_id,Reservation.starttime,Reservation.finishtime,Reservation.seatNum).filter(Reservation.starttime == now).order_by(Reservation.starttime).all()
    if seatInfoinput is not None: 
        for i in range(len(seatInfoinput)):
            data1 = Seat.query.filter(Seat.seatNum == seatInfoinput[i][3]).first()
            user_id = seatInfoinput[i][0]
            used = 1
            finish_time = seatInfoinput[i][2]
                
            data1.user_id = user_id
            data1.used = used
            data1.finish_time = finish_time
            db.session.commit()

    # 유저가 사용이 끝나는 시간이 되어 Seat 테이블을 최신화 해주는 경우
    seatInfooutput = db.session.query(Seat.user_id,Seat.finish_time,Seat.seatNum).filter(Seat.finish_time == now).order_by(Seat.finish_time).all()
    if seatInfooutput is not None:
        for j in range(len(seatInfooutput)):
            data2 = Seat.query.filter(Seat.seatNum == seatInfooutput[j][2]).first()
            user_id = None
            used = 0
            finish_time = None

            data2.user_id = user_id
            data2.used = used
            data2.finish_time = finish_time
            db.session.commit()

    return "success"

def recommend(distance, acheater, windowfar, door): # 좌석 추천 알고리즘
    reclist = [x for x in range(1, 25)]
    seatlist = db.session.query(Seat.used).all()

    if distance: # Prefer 클래스의 distance가 True면 조건문이 실행됨
        for i in range(1, 25):
            if (i==1) and (seatlist[i-1][0] == True):
                for k in [i, i+1, i+2, i+3]:
                    if k in reclist: reclist.remove(k)

            if (i==2 or i==10) and (seatlist[i-1][0] == True):
                for k in [i-1, i, i+1, i+2, i+7, i+9]:
                    if k in reclist: reclist.remove(k)
            
            if (i==3 or i==5 or i==11 or i==13 or i==19 or i==21) and (seatlist[i-1][0] == True):
                for k in [i-2, i-1, i, i+1, i+2, i+3]:
                    if k in reclist: reclist.remove(k)
            
            if (i==4 or i==6 or i==12 or i==14) and (seatlist[i-1][0] == True):
                for k in [i-3, i-2, i-1, i, i+1, i+2, i+5, i+7, i+9]:
                    if k in reclist: reclist.remove(k)
            
            if (i==7) and (seatlist[i-1][0] == True):
                for k in [i-2, i-1, i, i+1]:
                    if k in reclist: reclist.remove(k)

            if (i==8 or i==16) and (seatlist[i-1][0] == True):
                for k in [i-3, i-2, i-1, i, i+5, i+7]:
                    if k in reclist: reclist.remove(k)
            
            if (i==9 or i==17) and (seatlist[i-1][0] == True):
                for k in [i-7, i-5, i, i+1, i+2, i+3]:
                    if k in reclist: reclist.remove(k)
            
            if (i==15 or i==23) and (seatlist[i-1][0] == True):
                for k in [i-9, i-7, i-2, i-1, i, i+1]:
                    if k in reclist: reclist.remove(k)
                    
            if (i==18) and (seatlist[i-1][0] == True):
                for k in [i-1, i, i+1, i+2]:
                    if k in reclist: reclist.remove(k)  
                    
            if (i==20 or i==22) and (seatlist[i-1][0] == True):
                for k in [i-3, i-2, i-1, i, i+1, i+2]:
                    if k in reclist: reclist.remove(k)  
                    
            if (i==24) and (seatlist[i-1][0] == True):
                for k in [i-3, i-2, i-1, i]:
                    if k in reclist: reclist.remove(k)    
                
    if acheater:
        for k in [21, 22, 23, 24]:
            if k in reclist:
                reclist.remove(k)

    if windowfar:
        for k in [1, 3, 5, 7, 8, 15, 16, 23, 24]:
            if k in reclist:
                reclist.remove(k)
        
    if door:
        for k in [17, 18, 19, 20]:
            if k in reclist:
                reclist.remove(k)

    return reclist # 추천하는 seat의 num 리스트를 return