from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
import app.functions.calculate as cal
import app.functions.functions as fun
import time
import threading
from requests.models import HTTPError
import random
# 추가할 모듈이 있다면 추가

main= Blueprint('main', __name__, url_prefix='/')

'''
미미또또님이 로비에 참가하셨습니다.
흑백화님이 로비에 참가하셨습니다.
보라돌이 앙앙님이 로비에 참가하셨습니다.
우물쭈물대지마라님이 로비에 참가하셨습니다.
Darius ever only님이 로비에 참가하셨습니다.
'''

'''
fun.calcualteScorePerUser(유저명)함수가 반환하는 결과입니다!
    resultSet = {
        "userName" : String,
        "championName" : [0~19],
        "teamPosition" : [0~19],
        "teamPositionKR" : [0~19],
        "deathKingCount" : INT,
        "badItemCount" : INT,
        "badSpellCount" : INT,
        "weakDamageCount" : INT,
        "lackGoldCount" : INT,
        "visionLowCount" : INT,
        "trollScore" : [0~19]
        "totalScore" : INT
    }
'''
@main.route('/test', methods = ['GET'])
def testPage() :
    value = []
    photo = "joker"
    for i in range(5) :
        value.append(random.randint(0, 150))
    return render_template('/replace.html', value = value, photo = photo)

@main.route('/', methods = ['GET'])
def mainPage() :
    return render_template('dodgecall-홈페이지.html')

@main.route('/home', methods = ['POST'])
def homePage():
    inputData = request.form["identification"]
    userNames = fun.nameSlice(inputData)

    try :
        start_time = time.time()
        infoList = []
        threads = []
        averageScore = 0
        for id in userNames :
            t = threading.Thread(target = cal.calculateScorePerUser, args = (id, infoList))
            t.start()
            threads.append(t)

        for t in threads :
            t.join()

        for i in range(len(infoList)) :
            averageScore += infoList[i]['totalScore']
        
        averageScore /= len(infoList)
        averageScore = round(averageScore, 1)
    except HTTPError as e:
        print("에러 발생 :", e)
        return render_template('dodgecall-홈페이지.html')
    
    print("총 소요 시간 :", time.time() - start_time)
    return render_template('/replace.html', result = infoList, averageScore = averageScore)