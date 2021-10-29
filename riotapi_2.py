from requests.models import HTTPError
from riotwatcher import LolWatcher
from riotwatcher._apis.league_of_legends.MatchApiV5 import MatchApiV5
import json


key= 'RGAPI-688191e7-0526-40b4-b0bf-982eb9fea12f' #제한시간 1일
watcher = LolWatcher(key)
id=[]
matchid=[]
matchData={}
fileNum=0
idCount=0
with open('test.json','r',encoding='utf-8') as f:
    data = json.load(f)

for key in data.keys():
    id.append(key)
    idCount=idCount+1

for value in data.values():
    matchid.append(value)
print(matchid[0])

for i in range(0,idCount,1):
    length = len(matchid[i]) ## 매치가 20개가 아닌 경우
    for j in range(0,length):
        try:
            if value=='Error':
                continue
            else:
                print(matchid[i][j])
                matchData=watcher.match_v5.by_id('ASIA',matchid[i][j])
                with open ('matchData'+str(fileNum)+'.json','w',encoding='utf-8') as outfile: ## 딕셔너리 json으로 인코딩 후 저장
                     json.dump(matchData,outfile,ensure_ascii=False,indent=4)
                fileNum=fileNum+1

        except HTTPError as e:
             print('Error')







