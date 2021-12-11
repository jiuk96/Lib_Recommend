# 파일 실행, DB 위치 관련 파일

# created by 장지욱 11.09
# modified by 장지욱 12.06 apscheduler 모듈을 사용해서 매 30분마다 코드 자동실행하여 Seat 테이블 정보 최신화해주기

from flask import Flask
from api import *
from db_connect import db
from flask_bcrypt import Bcrypt
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/library_recommend"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = 'asodfajsdofijac'

db.init_app(app)
bcrypt = Bcrypt(app)

sched = BackgroundScheduler(daemon=True)
sched.start()

# 매일 밤 12시가 되면 Seat 테이블 정보를 초기화 해준다. 
@sched.scheduled_job('cron', hour='0', minute='00', id='test_1')
def seat_initailze_atnight():
    with app.app_context():
        seat_initialize()

# 10초마다 코드 자동실행하여 Seat 테이블 정보 최신화해주기
@sched.scheduled_job('interval', seconds=10, id='test_2')
def seat_update_every10sec():
    #print(f'job1 : {time.strftime("%H:%M:%S")}') #정상 작동하는지 체크
    with app.app_context():
        seat_update()

# 매 30분마다 코드 자동실행하여 Seat 테이블 정보 최신화해주기 (07:00~22:30분까지 30분 주기로 체크)
#@sched.scheduled_job('cron', hour='7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22', minute='30,00', id='test_2')
#def seat_update_every_30minutes():
#    with app.app_context():
#        seat_update()

# 도중에 홈페이지 꺼지면 끝
atexit.register(lambda: sched.shutdown(wait=False))

if __name__ == '__main__':
    app.run(debug=True)
