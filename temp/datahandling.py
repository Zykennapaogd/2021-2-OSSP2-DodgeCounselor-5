import json
import pyrebase
from datetime import datetime, time
import sys

def DeathKing(i):
    #데스수가 게임시간-5 보다 크거나 같으면 대가리 박은걸로 간주
    if death_count[i]>=gameDuration-5:
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

def DoneDamage(i):
    pos=position[i]
    damage=(int)(damage_list[i])
    index=0
    if pos=='UTILITY': #서폿은 나가있어
        return 0

    # 자신과 같은 position의 딜량찾기
    if i<5:
        for j in range(5,10):
            if position[j]==pos:
                index=j
                #print(index)
                break
    else:
         for j in range(0,10):
            if position[j]==pos:
                index=j
                #print(index)
                break

    # 같은 포지션의 두명 비교해서 딜량이 절반보다 작으면  
    dmgDiff = damage_list[index] / damage      
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

def goldDiffByPostion(i):
    pos=position[i]
    index=0
    if pos=='UTILITY': #서폿은 나가있어
        return 0
    gold = int(goldbyposition[i])
    if i<5:
        for j in range(5,10):
            if position[j]==pos:
                index=j
                #print(index)
                break
    else:
         for j in range(0,10):
            if position[j]==pos:
                index=j
                #print(index)
                break
    diff = int(goldbyposition[index])/gold # 상대가 획득한 골드 / i 번째 플레이어가 획득한 골드
    print('골드차이:' + str(diff))
    if diff>=2:
        return 5
    else: 
        return 0

""" def visionWardsBought(i): 
    if visionWards[i] == 0: #제어와드 구매횟수가 0인 경우
        return 5
    else:
        return 0 """

""" def noSupItem(i):
    number = ['0','1','2','3','4','5']
    sup_item = [3850,3851,3853,3854,3855,3857,3858,3859,3860,3862,3863,3864] # 현 버전 서폿템 리스트
    itemlist=[]
    count = 0
    if position[i] == 'UTILITY': #서폿인경우
        for num in number:
            itemlist.append(matchData['info']['participants'][i]['item'+num])
    else: #그외
        return 0
    print(itemlist)
    for item in itemlist: #아이템0~아이템5 
        for sitem in sup_item: #서폿템 
            if item == sitem: #서폿템이 있으면
                return 0
            else:
                continue

    print("서폿템 없다")
    return 5 #서폿템이 없는 경우 """
   
            



    

###시작

#DB연결
with open("auth.json") as f:
    config = json.load(f)

firebase = pyrebase.initialize_app(config)
db = firebase.database()
file_number=0
starttime = datetime.today()
division = ['I','II','III','IV']
page = ['1','2','3']
index=0
while(True):
   
    
    # matchData 불러오기. 이후에 반복문으로 바꿔야함 0부터 시작해서 없을때까지 반복
    # if file_number == 19:
    #      print(u)
    #      break


    try:     
        with open('./SILVER I _ IV/SILVER '+division[index]+' Page '+page[0]+'/matchData'+str(file_number)+'.json','r',encoding='utf-8') as f:
            global matchData
            matchData=json.load(f)
    except FileNotFoundError:
        if index==3:
            sys.exit("끝")
        else:
            index = index+1
            file_number = 0

    
    
    print('./SILVER I _ IV/SILVER '+division[index]+' Page '+page[0]+'/matchData'+str(file_number)+'.json')
    file_number=file_number+1   

    list_name=[]    ## 유저의 아이디
    death_count=[]  ## 유저의 데스수
    damage_list=[]  ## 적에게 가한 데미지
    position=[]  ## 실제 게임에서 플레이한 포지션
    goldbyposition=[] ## 포지션별 골드획득량 
    
    

    for i in range(0,10,1):  ## 10명의 소환사명 데스수 데미지 포지션 리스트에 저장
        list_name.append(matchData['info']['participants'][i]['summonerName']) 
        damage_list.append(matchData['info']['participants'][i]['totalDamageDealtToChampions'])
        death_count.append(matchData['info']['participants'][i]['deaths']) 
        position.append(matchData['info']['participants'][i]['teamPosition'])
        goldbyposition.append(matchData['info']['participants'][i]['goldEarned'])

        
        
        
    print(list_name)
    print(damage_list)
    print(death_count)
    print(position)
    print(goldbyposition)

    

  
    if 'gameEndTimestamp' in matchData['info']:
        #print("yes")
        gameDuration =  int(matchData['info']['gameEndTimestamp']) - int(matchData['info']['gameStartTimestamp'])
    else:
        #print("no")
        gameDuration = int(matchData['info']['gameDuration'])
   
    
    gameDuration = gameDuration/1000
    gameDuration = int(gameDuration/60)
    print("게임시간: " + str(gameDuration) + " 분")
    

    


    for i in range(0,10,1):
        if gameDuration<15: #탈주로 인해 15분전에 게임이 끝나는 경우는 제외
            break
        user = db.child("users").order_by_child("id").equal_to(list_name[i]).get()
        dic = user.val()
        if len(dic) != 0: # 기존에 존재하면
            dmg = DoneDamage(i)
            spell = spellCheck(i)
            noitem = Noitem(i)
            death = DeathKing(i)
            gold= goldDiffByPostion(i)
            total = dmg+spell+noitem+death+gold
            death = death + dic[list_name[i]]['DeathKing']
            noitem = noitem + dic[list_name[i]]['No_Item']
            spell = spell + dic[list_name[i]]['SpellCheck'] 
            dmg = dmg + dic[list_name[i]]['DoneDamage']
            gold= gold + dic[list_name[i]]['goldDiffer']
            total = total + dic[list_name[i]]['Total_Points'] 
            data = {"id":list_name[i],'DeathKing':death, 'No_Item':noitem, 'SpellCheck':spell,'DoneDamage':dmg,'goldDiffer':gold,'Total_Points':total}
            db.child("users").child(list_name[i]).update(data) 

        else:
            dmg= DoneDamage(i)
            spell=spellCheck(i)
            noitem = Noitem(i)
            death = DeathKing(i)
            gold= goldDiffByPostion(i)
            total = dmg+spell+noitem+death+gold
            data = {"id":list_name[i],'DeathKing':death, 'No_Item':noitem, 'SpellCheck':spell,'DoneDamage':dmg,'goldDiffer':gold,'Total_Points':total}
            db.child("users").child(list_name[i]).set(data)
 
    endtime = datetime.today()
    print('시작시간: '+str(starttime))
    print('완료시간: '+str(endtime))     



        

































































































   





    

    










