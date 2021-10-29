from requests.models import HTTPError
from riotwatcher import LolWatcher
from riotwatcher._apis.league_of_legends.MatchApiV5 import MatchApiV5
from riotwatcher._apis.league_of_legends.SummonerApiV4 import SummonerApiV4
from riotwatcher._apis.league_of_legends.LeagueApiV4 import LeagueApiV4
import json
key= 'RGAPI-688191e7-0526-40b4-b0bf-982eb9fea12f' #제한시간 1일
watcher = LolWatcher(key)
#puuid= 'LUXX8kbYtBaOsnrAlfrgaI2vO4-tsn135UiWQsztQMJI6-E_DA_wuKlVhNQPajHcYmaKZSTVAuMJaQ'

#def printStats(summonerName):
    # summoner = watcher.summoner.by_name('kr',summonerName)
    # stats = watcher.league.by_summoner('kr',summoner['id'])
    # matchlist = watcher.match_v5.matchlist_by_puuid('asia',summoner['puuid']) # puuid로 matchid 가져오기

    # tier = stats[0]['tier']
    # rank = stats[0]['rank']
    # lp = stats[0]['leaguePoints']
    # wins = int(stats[0]['wins'])
    # losses = int(stats[0]['losses'])
    # winrate = int((wins / (wins+ losses))*100)
    # print(matchlist)
    # print(summoner)
    # print(summoner['puuid'])
    # print(tier,rank,lp)
    # print(str(winrate) + "%")
    # print(summonerName+" is currently ranked in "+str(tier)+" " +str(rank) +" with "+str(lp) +" LP and a "+str(winrate)+"% winrate")



# 소환사명 가져오기
players = watcher.league.entries('KR','RANKED_SOLO_5x5','BRONZE','I',1) ##리스트로 저장됨
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
        #print(summoner['puuid'])
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
            matchlist = watcher.match_v5.matchlist_by_puuid('asia',i,None,20,None,"ranked")
            matchidList.append(matchlist)

    except HTTPError as e:
        matchidList.append("Error")



for i in matchidList:
    print(i)

dic = { name:value for name,value in zip(playerList,matchidList)} ## 아이디랑 matchid 묶어서 dictionary 만듬
print(dic)
print("")
print(dic[playerList[0]])


with open ('test.json','w',encoding='utf-8') as outfile: ## 딕셔너리 json으로 인코딩 후 저장
  json.dump(dic,outfile,ensure_ascii=False,indent=4)

  
print("끝")

    


#print(summonerList)


     



#printStats("중소기업질병게임")



