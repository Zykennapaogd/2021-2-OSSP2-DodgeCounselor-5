import json
import os

TIER = "SILVER"
DIVISION = "IV"

positionList = [
    "TOP",
    "JUNGLE",
    "MIDDLE",
    "BOTTOM",
    "UTILITY"
]

#2차원 리스트로 구성, 각 리스트는 위의 positionList를 위한 위치임
infoList = [
    [],
    [],
    [],
    [],
    []
]

page = 1
fileNum = 0

if not os.path.exists("./DataList/" + TIER + " " + DIVISION + " Page " + str(page)) :
    print("해당하는 Tier, Division의 데이터가 없습니다")
    quit()

while True :

    path = "./DataList/" + TIER + " " + DIVISION + " Page " + str(page)
    filePath = path + "/matchData" + str(fileNum) + ".json"

    try :
        with open(filePath, 'r', encoding='UTF8') as f :
            data = json.load(f)

            #진행상황이 좀 보이도록 출력부분 생성
            if (fileNum % 500 == 0) :
                print(filePath, "분류 시작")
            

    except :    #찾지 못한 경우 해당 page에 대한 결과를 모두 분석한 경우임
        if not os.path.exists(path) :    #추가적인 page가 존재하지 않는다면 출력하고 종료
            print(TIER, DIVISION, "에 해당하는 유저들의 결과를", str(page - 1), "페이지까지 분류하였습니다")
            for i in range (len(positionList)) :
                print(positionList[i], ":", + len(infoList[i]), "명")
            break
        else :  #page가 남아있다면 다음으로 진행
            print("Page", page, "분류 완료")
            page += 1
            fileNum = 0
            continue   
    
    for i in range(10) :    #한 게임에는 플레이어가 10명씩 존재하므로 for문은 10번 반복
        userInfo = data['info']['participants'][i]
        position = userInfo['teamPosition']

        #position 값에 따라 적절한 List에 추가하기
        if (position == positionList[0]) :  #TOP
            infoList[0].append(userInfo)

        elif (position == positionList[1]) :    #JUNGLE
            infoList[1].append(userInfo)

        elif (position == positionList[2]) :    #MIDDLE
            infoList[2].append(userInfo)

        elif (position == positionList[3]) :    #BOTTOM
            infoList[3].append(userInfo)

        elif (position == positionList[4]) :    #UTILITY
            infoList[4].append(userInfo)
    fileNum += 1

#end while, while문이 끝나면 찾아놓은 데이터에 대한 기록이 끝난 것

#결과 저장할 폴더가 없다면 일단 만들고
if not os.path.exists("./ResultSet") :
    os.makedirs("./ResultSet")

#결과 저장
for i in range(5) :
    outPath = "./ResultSet/" + TIER + " " + DIVISION + " " + positionList[i] + ".json"
    with open(outPath,'w',encoding='utf-8') as outfile:
        json.dump(infoList[i], outfile, ensure_ascii=False,indent=4)

print("파일이 생성되었습니다")