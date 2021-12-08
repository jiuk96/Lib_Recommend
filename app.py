# 파일 실행, DB 위치 관련 파일

# created by 장지욱 11.09

# import time
import pymysql
from flask import Flask
from api import *
from db_connect import db
from flask_bcrypt import Bcrypt
# from apscheduler.schedulers.background import BackgroundScheduler
# import atexit

app = Flask(__name__)
app.register_blueprint(board)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/Library_recommend"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = 'asodfajsdofijac'

db.init_app(app)
bcrypt = Bcrypt(app)

# with app.app_context():
#     db.create_all()

# sched = BackgroundScheduler(daemon=True)
# sched.start()

# @sched.scheduled_job('interval', seconds=20, id='test_1')
# def job1():
#     print(f'job1 : {time.strftime("%H:%M:%S")}')
    # seat_update()

# @sched.scheduled_job('cron', hour='12,13,14,15,16,17', minute='48', id='test_2')
# def seat_update_every_30minutes():
#     seat_update()


# atexit.register(lambda: sched.shutdown(wait=False))

if __name__ == '__main__':
    app.run(debug=True)
