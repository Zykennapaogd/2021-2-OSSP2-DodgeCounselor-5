# file name : index.py
# pwd : /project_name/app/main/index.py
 
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
import app.functions.calculate as fun
import app.functions.functions
import time as t
# 추가할 모듈이 있다면 추가
 
main= Blueprint('main', __name__, url_prefix='/')

'''
fun.calcualteScorePerUser(유저명)함수가 반환하는 결과입니다!
    resultSet = {
        "deathKingCount" : INT,
        "badItemCount" : INT,
        "badSpellCount" : INT,
        "weakDamageCount" : INT,
        "lackGoldCount" : INT,
        "visionLowCount" : INT,
        "trollScore" : [0~20]
        "totalScore" : INT
    }
'''

@main.route('/', methods = ['GET'])
def mainPage():
    userName = [
        "T1 Roach",
        "Hide on bush",
        "미안합니다sry",
        "Hakunaa Matata",
        "쪼렙이다말로하자"
    ]
    start_time = t.time()
    for i in range(len(userName)) :
        print((i+1),"번째 시작, 소요 시간 : ", round(t.time() - start_time, 3), "초")
        fun.calculateScorePerUser(userName[i])

    return render_template('/dodgecall-홈페이지.html')

@main.route('/home', methods = ['GET'])
def homePage():
      return render_template('측정결과창.html')