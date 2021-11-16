import json
import pyrebase

def DeathKing(i):
    #데스수가 게임시간-5 보다 크거나 같으면 
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
    if damage<=((int)(damage_list[index])/2):
        return 5
    else:
        return 0
    

###시작

#DB연결
with open("auth.json") as f:
    config = json.load(f)

firebase = pyrebase.initialize_app(config)
db = firebase.database()

file_number=1

while(True):
    # matchData 불러오기. 이후에 반복문으로 바꿔야함 0부터 시작해서 없을때까지 반복
    with open('./matchData_Bronze1(10.29)/matchData'+str(file_number)+'.json','r',encoding='utf-8') as f: 
        global matchData
        matchData=json.load(f)
        file_number=file_number+1

    list_name=[]    ## 유저의 아이디
    death_count=[]  ## 유저의 데스수
    damage_list=[]  ## 적에게 가한 데미지
    position=[]  ## 실제 게임에서 플레이한 포지션

    for i in range(0,10,1):  ## 10명의 소환사명 데스수 데미지 포지션 리스트에 저장
        list_name.append(matchData['info']['participants'][i]['summonerName']) 
        damage_list.append(matchData['info']['participants'][i]['totalDamageDealtToChampions'])
        death_count.append(matchData['info']['participants'][i]['deaths']) 
        position.append(matchData['info']['participants'][i]['teamPosition'])
        
    print(list_name)
    print(damage_list)
    print(death_count)
    print(position)

    #death_count.pop(0)
    #print(death_count)
    #death_count.insert(0,34)
    #print(death_count)
    # print(matchData['info']['gameDuration'])  한줄주석 컨트롤K + 컨트롤C
    gameDuration = int(matchData['info']['gameDuration'])
    gameDuration = gameDuration/1000
    gameDuration = int(gameDuration/60)
    print(gameDuration)


    for i in range(0,10,1):
        dmg= DoneDamage(i)
        spell=spellCheck(i)
        noitem = Noitem(i)
        death = DeathKing(i)
        total = dmg+spell+noitem+death
        data = {"id":list_name[i],'DeathKing':death, 'No_Item':noitem, 'SpellCheck':spell,'DoneDamage':dmg,'Total_Points':total}
        db.child("users").child(list_name[i]).set(data)































#블럭주석 ALT + SHIFT + A
""" trollDB={'Player': [{   'summonerName':' ',  
                        'DeathKing':' ', 
                        'No_Item':' ', 
                        'SpellCheck':' ',
                        'DoneDamage':' ',
                        'Total_Points':' '}]
     
        }

trollDB_copy={          'summonerName':' ',
                        'DeathKing':' ', 
                        'No_Item':' ', 
                        'SpellCheck':' ',
                        'DoneDamage':' ',
                        'Total_Points':' '}
     
# 중복되는 소환사명이 있으면 append 안함. 대신 Player value의 리스트 번호를 저장       
for i in range(0,10,1):
    trollDB['Player'].append(dict(trollDB_copy)) # value에 딕셔너리형 리스트 추가 *dict()안하면 레퍼런스만 복사됨 아오 시발*
    

#실제 트롤력 계산 및 DB 업데이트
for i in range(0,10,1):
    trollDB['Player'][i]['summonerName'] = list_name[i]
    #trollDB['Player'][i]['Total_Points'] = i
    death = DeathKing(i)
    trollDB['Player'][i]['DeathKing'] = death
    item = Noitem(i)
    trollDB['Player'][i]['No_Item'] = item
    spell = spellCheck(i)
    trollDB['Player'][i]['SpellCheck'] = spell
    damage = DoneDamage(i)
    trollDB['Player'][i]['DoneDamage'] = damage
    total = 0
    total = death+item+spell+damage
    trollDB['Player'][i]['Total_Points'] = total

   

#print(len(trollDB['Player']))
with open ('handlingData.json','w',encoding='utf-8') as outfile: ## 딕셔너리 json으로 인코딩 후 저장
  json.dump(trollDB,outfile,ensure_ascii=False,indent=4) """










   





    

    










