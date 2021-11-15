import functions
import time       
GAMECOUNT = 5   #몇 게임에 대한 정보를 불러올지를 정하는 변수입니다. 수정하셔서 사용하시면 됩니다.
    
# 멀티서치용 예시입니다
# VSCode 기준 Ctrl + K, Ctrl + U 하고 사용하시고, Ctrl + K, Ctrl + C하셔서 다시 주석처리 하시면 됩니다
# 빡 베 인님이 로비에 참가하셨습니다.
# 우물쭈물대지마라님이 로비에 참가하셨습니다.
# 감비아사무총장님이 로비에 참가하셨습니다.
# 오억이님이 로비에 참가하셨습니다.
# Dake님이 로비에 참가하셨습니다.

# main start
playerList = [] #유저의 이름이 담길 리스트
infoList = [] #이름에 대한 SummonerDTO가 담길 리스트
matchList = [] #각 유저별 20게임씩의 데이터가 담길 리스트
matchInfo = []  #게임 데이터가 담길 리스트
analyzedResult = [] #유저별 트롤력 분석에 필요한 정보가 담긴 리스트

playerList = functions.nameSlice()
start = time.time()

infoList = functions.getSummonerInfo(playerList)
matchList = functions.getMatchBySummonerDTO(infoList, GAMECOUNT)
matchInfo = functions.getMatchInfoByMatchID(matchList)

for i in range(5) : #analyzedResult에 게임 정보 각각을 저장
    analyzedResult.append(functions.analyzeGames(infoList[i]['puuid'], matchInfo[i]))




# 유저들의 이름이 제대로 긁어졌는지 확인하기 위해 출력해본 코드입니다.
for i in range(len(playerList)) :
    print(i + 1 , "번째 플레이어 이름은 ", playerList[i], "입니다.")
print("\n")

#확보한 infoList에 문제가 없는지 확인해보기 위해 출력해본 코드입니다
for i in range(len(infoList)) :
    print(i + 1, "번째 유저의 유저명은 " , infoList[i]['name'], "이고, puuid는 ", infoList[i]['puuid'], "입니다")
print("\n")

# 확보한 MatchID를 확인해보기 위해 출력해본 코드입니다
for i in range(len(matchList)) :
    print(i + 1, "번째 유저의 정보입니다")
    for j in range(len(matchList[i])) :
        print(j + 1, "번째 MatchID : ", matchList[i][j])
print("\n")        

#확보한 트롤력 측정을 위한 정보의 확인을 위해 출력해본 코드입니다
for i in range (len(analyzedResult)) :
    print(i + 1, "번째 플레이어의", len(matchInfo[i]), "회의 게임에 대한 정보입니다")
    print("팀원 평균 이상 데스한 횟수 : ", analyzedResult[i]['overDeath'])
    print("같은 아이템을 3개 이상 산 횟수 : ", analyzedResult[i]['sameItems'])
    print("적절하지 않은 스펠을 사용한 게임의 횟수 : ", analyzedResult[i]['incorrectSpell'])
    
    for j in range(len(matchInfo[i])) :
        print(j + 1 , "번째 게임의 길이 : ", analyzedResult[i]['gameLengthPerGame'][j], "분")
        print(j + 1 , "번째 게임에서 설치한 와드의 수 : ", analyzedResult[i]['wardPlacedPerGame'][j])
        print(j + 1 , "번째 게임에서 벌어들인 골드의 양 : ", analyzedResult[i]['goldEarnedPerGame'][j])
        print(j + 1 , "번째 게임에서 소모한 골드의 양 : ", analyzedResult[i]['goldSpentPerGame'][j])
        print(j + 1 , "번째 게임에서 사용한 챔피언 이름 : ", analyzedResult[i]['championNamePerGame'][j])
        print(j + 1 , "번째 게임의 승패 여부 : ", analyzedResult[i]['weatherWinPerGame'][j], "\n")
    print("\n")


print("총 소요 시간 : ", round(time.time() - start, 2), "초")