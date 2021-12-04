from requests.models import HTTPError
from riotwatcher import LolWatcher
import time
from time import sleep
import threading
import pyrebase
import json

key= 'RGAPI-5331f938-1662-4395-a71f-960c658f5922' # Personal Key 분당 100개 request
watcher = LolWatcher(key)


def DeathKing(death,gameDuration):
    #데스수가 게임시간-5 보다 크거나 같으면 대가리 박은걸로 간주
    if death>=gameDuration-5:
        return 5
    else:
        return 0

def Noitem(i):
    number = ['0','1','2','3','4','5']
    count_no_item=0
    count_same_item = 0
    item_list=[]
    last_item = -1
    for num in number:
        item_list.append(matchData['info']['participants'][i]['item'+num])
        if matchData['info']['participants'][i]['item'+num] != 0:  #아이템이 있는경우 
            #print(matchData['info']['participants'][i]['item'+num])
            continue
        else: #아이템이 없는 경우
            count_no_item=count_no_item+1

    for i in range (0,6,1): #아이템이 같으면 
        if last_item == item_list[i]:
            count_same_item=count_same_item+1
        last_item = item_list[i]


    #템창의 아이템이 모두 같거나 하나도 없는경우
    if count_no_item==5 or count_same_item==5:
        return 5
    else:
        return 0

def spellCheck(i):
    if matchData['info']['participants'][i]['teamPosition'] == 'JUNGLE': #정글이 강타 안든 경우
        if (int)(matchData['info']['participants'][i]['summoner1Id']) == 11 or (int)(matchData['info']['participants'][i]['summoner2Id']) == 11:
            return 0
        else:
            return 5
    else:
        return 0

def DoneDamage(i,role,dmg):
    #pos=position[i]
    #damage=(int)(damage_list[i])
    index=0
    if role=='UTILITY': #서폿은 나가있어
        return 0

    # 자신과 같은 position의 딜량찾기
    if i<5:
        for j in range(5,10):
            if matchData['info']['participants'][j]['teamPosition']==role:
                index=j
                break
    else:
         for j in range(0,10):
            if matchData['info']['participants'][j]['teamPosition']==role:
                index=j
                break

    # 같은 포지션의 두명 비교해서 딜량이 절반보다 작으면
    enemydmg = matchData['info']['participants'][index]['totalDamageDealtToChampions']
    try:  
        dmgDiff = int(enemydmg) / dmg
    except ZeroDivisionError: #딜량이 0인 경우가 있었음. 명백한 트롤 15분 게임이였음
        return 25      
    if dmgDiff >= 5:
        return 25
    elif dmgDiff >= 4:
        return 20
    elif dmgDiff >= 3:
        return 15
    elif dmgDiff >= 2.5:
        return 10
    elif dmgDiff >= 2:
        return 5
    else:
        return 0

def goldDiffByPostion(i,role,gold):
    #pos=position[i]
    index=0
    if role=='UTILITY': #서폿은 나가있어
        return 0
    #gold = int(goldbyposition[i])
    if i<5:
        for j in range(5,10):
            if matchData['info']['participants'][j]['teamPosition']==role:
                index=j
                break
    else:
         for j in range(0,10):
            if matchData['info']['participants'][j]['teamPosition']==role:
                index=j
                break
    
    enemygold = matchData['info']['participants'][index]['goldEarned']
    diff = int(enemygold)/gold # 상대가 획득한 골드 / i 번째 플레이어가 획득한 골드
    #print('골드차이:' + str(diff))
    if diff>=2:
        return 5
    else: 
        return 0

def getGameDuration(matchData):

    gameDuration=0

    if 'gameEndTimestamp' in matchData['info']:
        gameDuration =  int(matchData['info']['gameEndTimestamp']) - int(matchData['info']['gameStartTimestamp'])
    else:
        gameDuration = int(matchData['info']['gameDuration'])
   
    gameDuration = gameDuration/1000
    gameDuration = int(gameDuration/60)

    return gameDuration


def getLatestMatches(id):
    
    gameDuration=0
    score=[0,0,0,0,0,0] # 계산한 모든 점수를 합산하기 위한 리스트 0번 deathking부터 6번 total 까지 
    summoner = watcher.summoner.by_name('KR',id) 
    matchlist = watcher.match_v5.matchlist_by_puuid('asia',summoner['puuid'],None,10,None,"ranked") # matchid 10개 불러옴
    global matchData
   
    for i in range(len(matchlist)):
        try:
                matchData=watcher.match_v5.by_id('ASIA',matchlist[i]) # matchid로 matchdata 가져옴
                gameDuration = getGameDuration(matchData)
                if gameDuration < 15: # 조기서렌은 계산 제외
                    continue
                else:
                    getScore(matchData,id,score,gameDuration)
        except HTTPError as e: # 429 Error 걸리면 완료까지 2분 걸림. 
            print(e)
  
    print(id+ "의 트롤력은: " + str(score))
    data = {"id":id,'DeathKing':score[0], 'No_Item':score[1], 'SpellCheck':score[2],'DoneDamage':score[3],'goldDiffer':score[4],'Total_Points':score[5]}
    db.child("users").child(id).set(data)
    print("DB 저장완료")


def getScore(matchData,id,score,gameDuration):
    
    index=0 #matchData info의 몇번째 participants인지 저장하는 변수 
    for i in range(0,10,1):
        if matchData['info']['participants'][i]['summonerName'] == id:
            index = i
            break
    death = matchData['info']['participants'][i]['deaths']
    dmg = matchData['info']['participants'][i]['totalDamageDealtToChampions']
    role = matchData['info']['participants'][i]['teamPosition']
    gold = matchData['info']['participants'][i]['goldEarned']

    deathking = DeathKing(death,gameDuration)
    noitem = Noitem(index)
    spell = spellCheck(index)
    donedmg = DoneDamage(index,role,dmg)
    golddiff = goldDiffByPostion(index,role,gold)
    total = deathking+noitem+spell+donedmg+golddiff
    score_var = [deathking,noitem,spell,donedmg,golddiff,total]

    for i in range(len(score)): #score 저장
        score[i] += score_var[i]

 
if __name__=='__main__':

    with open("auth.json") as f:
        config = json.load(f)
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    threads=[]  
    start = time.time()
    ids = ['좀 치는구나','민초충박멸','중소기업질병게임','쟤가범인','round6'] #웹에서 id 5개 받아왔다고 가정

    for id in ids: #DB에 해당 id가 없으면 쓰레드 생성 후 계산. 있으면 패스
        user = db.child("users").order_by_child("id").equal_to(id).get()
        dic = user.val()
        if len(dic)==0:
            print("DB에 없는 id: " + id)
            t = threading.Thread(target=getLatestMatches,args=(id,))
            threads.append(t)
            t.start()
        else: #DB에 있는 값 가져옴 이거 웹으로 보내주면 됨
            print("DB에 있는 id: "+ id)
            death = dic[id]['DeathKing']
            noitem = dic[id]['No_Item']
            spell =  dic[id]['SpellCheck'] 
            dmg = dic[id]['DoneDamage']
            gold= dic[id]['goldDiffer']
            total = dic[id]['Total_Points'] 

            

    # for id in ids:
    #     t = threading.Thread(target=getLatestMatches,args=(id,))
    #     threads.append(t)
    
    # for thread in threads:
    #     thread.start()

    for thread in threads:
        thread.join()

    delta_t = time.time()-start
    print("소요시간 :",delta_t)

    




    
