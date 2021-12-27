import calculate as cal
import functions as fun
import json
import os

#가져올 유저들의 풀 세팅 및 Key값 작성
#DIVISION은 I, II, III, IV로 작성
#PAGE는 int값으로 작성
TIER = "GOLD"
DIVISION = "II"
PAGE = 1

#저장할 폴더를 만드는 함수
def createFolder(folderName) :
    try :
        if not os.path.exists("./LearningData") :
            os.makedirs("./LearningData")

        if os.path.exists(folderName) :
            print("이미 같은 폴더가 존재합니다")
            quit()
        else :
            os.makedirs(folderName)
    except OSError:
        print ('Error: Creating directory. ' +  folderName)
        

#Main start

#생성할 폴더의 이름 설정
folderName = "LearningData/" + TIER + " " + DIVISION + " Page " + str(PAGE)

#저장할 폴더를 생성한다.
createFolder(folderName)

#특정 티어, 디비전, 페이지에 존재하는 유저들의 이름을 players에 저장
players = fun.getUserNames(TIER, DIVISION, PAGE)

resultSet = []

for i in range(len(players)) : #유저의 각 정보를 저장해서 파일 하나하나로 만들기
    try :
        cal.calculateScorePerUser(players[i], resultSet)
        with open (folderName + "/" + players[i] + ".json", "w", encoding = "utf-8") as outfile :
            json.dump(resultSet[i], outfile, ensure_ascii = False, indent = 4)
    except :
        continue