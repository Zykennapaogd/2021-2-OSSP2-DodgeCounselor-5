# file name : index.py
# pwd : /project_name/app/main/index.py
 
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
import app.functions.calculate as fun
import time
import threading
# 추가할 모듈이 있다면 추가
 
main= Blueprint('main', __name__, url_prefix='/')

'''
fun.calcualteScorePerUser(유저명)함수가 반환하는 결과입니다!
    resultSet = {
        "userName" : String,
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
def mainPage() :
    print("홈페이지 출력")
    return render_template('/dodgecall-홈페이지.html')

@main.route('/home', methods = ['POST'])
def homePage():
    print("측정결과창 출력")
    inputData = request.form["identification"]
    
    print(inputData)

    userNames = [
        "T1 Roach",
        "Hide on bush",
        "미안합니다sry",
        "Hakunaa Matata",
        "쪼렙이다말로하자"
    ]
    
    infoList = []

    start_time = time.time()
    
    threads = []
    for id in userNames :
        t = threading.Thread(target = fun.calculateScorePerUser, args = (id, infoList))
        t.start()
        threads.append(t)
    

    for t in threads :
        t.join()
    
    print("총 소요 시간 :", time.time() - start_time)
    return render_template('측정결과창.html',  result = infoList)