from requests.models import HTTPError
from riotwatcher import LolWatcher
from riotwatcher._apis.league_of_legends.MatchApiV5 import MatchApiV5
from riotwatcher._apis.league_of_legends.SummonerApiV4 import SummonerApiV4
from riotwatcher._apis.league_of_legends.LeagueApiV4 import LeagueApiV4
import json
import os

#가져올 유저들의 풀 세팅 및 Key값 작성
#DIVISION은 I, II, III, IV로 작성
#PAGE는 int값으로 작성
#Key도 여기에 입력하고 돌려주시면 됩니다!
KEY ='RGAPI-c404d684-2d9e-4143-a8f6-a600774bb17b'   #Production Key
TIER = "GOLD"
DIVISION = "II"
PAGE = 1

watcher = LolWatcher(KEY)

#저장할 폴더를 만드는 과정
def createFolder(folderName) :
    try :
        if not os.path.exists("./DataList") :
            os.makedirs("./DataList")

        if os.path.exists(folderName) :
            print("이미 같은 폴더가 존재합니다")
            quit()
        else :
            os.makedirs(folderName)
    except OSError:
        print ('Error: Creating directory. ' +  folderName)
    

#Main start

#생성할 폴더의 이름 설정
folderName = "./DataList/" + TIER + " " + DIVISION + " Page " + str(PAGE)

#저장할 폴더를 생성한다.
createFolder(folderName)

# 소환사명 가져오기
players = watcher.league.entries('KR','RANKED_SOLO_5x5', TIER, DIVISION, PAGE) ##리스트로 저장됨
print(len(players)) # 리스트 내의 player가 몇 명인지
print(players[12]['summonerName']) # 특정 번호 Player의 소환사명 가져오기 
playerList=[] # 가져온 플레이어들의 소환사명을 저장하기 위한 리스트
puuidList=[] # puuid 저장하기 위한 리스트
matchidList=[] #matchid 저장하기 위한 리스트
for i in range(len(players)):
 playerList.append(players[i]['summonerName'])

for i in playerList:
 print(i)

# puuid 가져오기
for i in playerList:
    try:
        summoner = watcher.summoner.by_name('kr',i)
        print(summoner['puuid'])
        puuidList.append(summoner['puuid'])
        
    except HTTPError as e:
        print('page not found')
        puuidList.append("Error")


for i in puuidList:
    print(i)

# matchid 가져오기
for i in puuidList:
    try:
        if i == "None":
            matchidList.append("None")
            continue
        else:
            matchlist = watcher.match.matchlist_by_puuid('asia',i,None,20,None,"ranked")
            matchidList.append(matchlist)

    except HTTPError as e:
        matchidList.append("Error")

for i in matchidList:
    print(i)

dic = { name:value for name,value in zip(playerList,matchidList)} ## 아이디랑 matchid 묶어서 dictionary 만듬
print(dic)
print("")
print(dic[playerList[0]])


with open (folderName + '/test.json','w',encoding='utf-8') as outfile: ## 딕셔너리 json으로 인코딩 후 저장
  json.dump(dic,outfile,ensure_ascii=False,indent=4)

outfile.close
  
print("끝")

id=[]
matchid=[]
matchData={}
fileNum=0
idCount=0
with open(folderName + '/test.json','r',encoding='utf-8') as f:
    data = json.load(f)

for key in data.keys():
    id.append(key)
    idCount=idCount+1

for value in data.values():
    matchid.append(value)
print(matchid[0])

for i in range(0,idCount,1):
    length = len(matchid[i]) ## 매치가 20개가 아닌 경우를 위해 len 수정
    for j in range(0,length):
        try:
            if value=='Error':
                continue
            else:
                print(matchid[i][j])
                matchData=watcher.match.by_id('ASIA',matchid[i][j])
                with open (folderName + '/matchData'+str(fileNum)+'.json','w',encoding='utf-8') as outfile: ## 딕셔너리 json으로 인코딩 후 저장
                     json.dump(matchData,outfile,ensure_ascii=False,indent=4)
                fileNum=fileNum+1

        except HTTPError as e:
             print('Error')

f.close
