from flask import Flask, render_template, url_for, session, request, redirect
from Post import *
from Seat import *
from User import *
app = Flask(__name__)


@app.route('/')
def login():
    pass

@app.route('/')
def logout():
    pass

@app.route('/')
def 회원가입():
    pass

@app.route('/')
def 좌석예약():
    pass

# @app.route('/')
# def 게시판 작성():
#   pass

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 