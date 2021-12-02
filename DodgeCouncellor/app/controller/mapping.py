# file name : index.py
# pwd : /project_name/app/main/index.py
 
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
import app.functions.calculate as fun
import app.functions.functions
# 추가할 모듈이 있다면 추가
 
main= Blueprint('main', __name__, url_prefix='/')

'''
fun.calcualteScorePerUser(유저명)함수가 반환하는 결과입니다!
    resultSet = {
        "deathKingCount" : 0,
        "badItemCount" : 0,
        "badSpellCount" : 0,
        "weakDamageCount" : 0,
        "lackGoldCount" : 0,
        "visionLowCount" : 0,
        "trollScore" : []
    }
'''

@main.route('/', methods = ['GET'])
def mainPage():
      userName = "우물쭈물대지마라"
      userInfo = fun.calculateScorePerUser(userName)

      print("4번째 판에서 계산된 트롤력 :", userInfo['trollScore'][0])

      

      return render_template('/dodgecall-홈페이지.html', returnValue = userInfo)

@main.route('/home', methods = ['GET'])
def homePage():
      return render_template('index.html')