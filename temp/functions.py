from requests.models import HTTPError
from riotwatcher import LolWatcher
from riotwatcher._apis.league_of_legends.SummonerApiV4 import SummonerApiV4
from riotwatcher._apis.league_of_legends.MatchApiV5 import MatchApiV5
key= '' #키 입력해주세요!
watcher = LolWatcher(key)

def nameSlice() :   #멀티서치 기능을 위해 사용되는 함수
    player = []
    print("입장 대화를 입력해주세요")
    for i in range(5) :
        player.append(input())
        for j in range(len(player[i])) :
            if (player[i][j] == '님') and (player[i][j+1] == '이') and (player[i][j+2] == " ") :    
                player[i] = player[i][0:j]
                break
    return player

def getUserNames(TIER, DIVISION, PAGE) :    #특정 티어, 디비전, 페이지의 유저명 모두 가져오기
    playerList=[] # 가져온 플레이어들의 소환사명을 저장하기 위한 리스트
    players = watcher.league.entries('KR','RANKED_SOLO_5x5', TIER, DIVISION, PAGE, ) #리스트로 저장됨

    for i in range(len(players)) :  #구해온 정보에서 소환사명만 빼서 저장
        playerList.append(players[i]['summonerName'])

    return playerList

def getSummonerInfo(playerName) :   #PlayerName을 이용하여 PlayerName에 따른 SummonerDTO를 반환해주는 함수
    infoList = []   #infoList에 플레이어들의 정보(SummonerDTO)가 리스트로 담김
    for i in range(len(playerName)) :
        infoList.append(watcher.summoner.by_name("KR", playerName[i]))  #입력받은 Playername들에 대하여 이름을 통한 SummonerDTO를 확보하여 infoList에 append.
    
    return infoList

def getMatchBySummonerDTO(infoList, gameCount) :     #SummonDTO에서 얻을 수 있는 puuid를 이용하여 최근 n개의 게임에 대한
    matchList = []
    for i in range(len(infoList)) :
        '''
        아래에 작성되어있는 matchList.append의 watcher함수 호출 부분의 매개변수 중 현재 10이라는 값을 가진 것이 유저별로 불러올 matchID의 갯수입니다
        20개로 하려 했는데, 20개로 하면 요청 제한에 걸리는 것인지 항상 120초 이상 걸립니다.
        그래서 10개로 일단 줄여놓은 상태입니다! 좋은 환경에서 다시 테스트하셔서 결과가 괜찮다면 20개씩 불러와도 될 것 같습니다.
        '''
        matchList.append(watcher.match.matchlist_by_puuid("asia", infoList[i]['puuid'], None, gameCount, None, "ranked"))   #Puuid를 이용하여 각 유저의 랭크게임 10개에 대한 MatchID 가져오기
    return matchList

def getMatchInfoByMatchID(matchList) :
    matchInfo = []
    eachPlayer = []
    for i in range(len(matchList)) :
        for j in range(len(matchList[i])) :
            eachPlayer.append(watcher.match.by_id('asia', matchList[i][j]))
        matchInfo.append(eachPlayer)
        eachPlayer = []
    return matchInfo


def getAverageDeath(singleMatchInfo, playerNum) :  #한 판의 경기에 대한 팀원의 평균 데스수를 계산하는 함수
    sumOfDeath = 0
    if playerNum < 5 :  #찾고자 하는 플레이어가 블루팀일 경우
        for i in range(5) : #0번부터 4번 플레이어의 데스 수 합산
            sumOfDeath += singleMatchInfo['info']['participants'][i]['deaths']
    else :  #찾고자 하는 플레이어가 레드팀일 경우
        for i in range (5, 10) : #5번부터 9번 플레이어의 데스 수 합산
            sumOfDeath += singleMatchInfo['info']['participants'][i]['deaths']

    return (sumOfDeath / 5)   #합산 반환


def buySameItems(singleMatchInfo, playerNum) : #어떤 게임에서 한 플레이어가 같은 아이템을 3개 이상 구매했는가?
    count = 0
    item = []
    item.append(singleMatchInfo['info']['participants'][playerNum]['item0'])
    item.append(singleMatchInfo['info']['participants'][playerNum]['item1'])
    item.append(singleMatchInfo['info']['participants'][playerNum]['item2'])
    item.append(singleMatchInfo['info']['participants'][playerNum]['item3'])
    item.append(singleMatchInfo['info']['participants'][playerNum]['item4'])
    item.append(singleMatchInfo['info']['participants'][playerNum]['item5'])

    for i in range(6) :
        for j in range(i + 1, 6) :
            if (item[i] == item[j] and item[i] != 0) :
                count += 1        

    return (True) if (count >= 3) else (False)


def UseCorrectSpell(singleMatchInfo, playerNum) : #한 게임에서 플레이어 포지션에 따른 스펠의 적절성 체크
    if singleMatchInfo['info']['participants'][playerNum]['teamPosition'] == "JUNGLE" : #포지션이 정글인 경우
        if singleMatchInfo['info']['participants'][playerNum]['summoner1Id'] == 11 or singleMatchInfo['info']['participants'][playerNum]['summoner2Id'] == 11 :
            return True     #강타 있으면 승패 상관없이 True
        else :
            return False    #정글러가 강타 없으면 승패 상관없이 False

    else :  #정글러가 아닌 경우
        if singleMatchInfo['info']['participants'][playerNum]['summoner1Id'] == 11 or singleMatchInfo['info']['participants'][playerNum]['summoner2Id'] == 11 :
            if (singleMatchInfo['info']['participants'][playerNum]['win']) :    
                return True     #정글러가 아닌데 강타 들었어도, 이겼으면 True
            else :
                return False    #정글러가 아닌데 강타 들고 졌으면? False

        else :  #강타 안들었으면 True
            return True


def getWardPlaced(singleMatchInfo, playerNum) :  #한 게임의 시야 점수를 확인.
    return (singleMatchInfo['info']['participants'][playerNum]['wardsPlaced'])

def getHowMuchGoldEarned(singleMatchInfo, playerNum) :  #한 게임의 벌어들인 골드 양을 확인. 
    return (singleMatchInfo['info']['participants'][playerNum]['goldEarned'])

def getHowMuchGoldSpent(singleMatchInfo, playerNum) :   #한 게임의 소모한 골드 양을 확인.
    return (singleMatchInfo['info']['participants'][playerNum]['goldSpent'])

def getGameWins(singleMatchInfo, playerNum) :           #한 게임의 승리 여부를 확인
    return (singleMatchInfo['info']['participants'][playerNum]['win'])

def getChampionName(singleMatchInfo, playerNum) :       #게임에서 사용한 챔피언 이름을 확인
    return (singleMatchInfo['info']['participants'][playerNum]['championName'])

def getGameLength(singleMatchInfo) :                    #각 게임의 길이 확인
    return (singleMatchInfo['info']['gameDuration'])

def analyzeGames(puuid, matchInfo) : #한명의 팀원에 대한 20게임을 평가하는 함수
    result = {
        "overDeath" : 0,
        "sameItems" : 0,
        "incorrectSpell" : 0,
        "gameLengthPerGame" : [],
        "wardPlacedPerGame" : [],
        "goldEarnedPerGame" : [],
        "goldSpentPerGame" : [],
        "weatherWinPerGame" : [],
        "championNamePerGame" : []
    }
        
    #리스트에 존재한 게임의 횟수만큼 반복
    for i in range (len(matchInfo)) :

        #게임에서 몇 번째 플레이어인지 playerNum에 저장
        for j in range (10) :   
            if puuid == matchInfo[i]['metadata']['participants'][j] :
                playerNum = j
        
        #팀 평균보다 더 많이 죽은 판이라면 overDeath값 1 증가
        averageDeath = getAverageDeath(matchInfo[i], playerNum)
        if averageDeath < matchInfo[i]['info']['participants'][playerNum]['deaths'] :
             result['overDeath'] += 1
        
        #같은 아이템을 3개 이상 샀다면 sameItems값 1증가
        if buySameItems(matchInfo[i], playerNum) :
            result['sameItems'] += 1
        
        #스펠이 불손하다면 incorrectSpell 1 증가
        if not(UseCorrectSpell(matchInfo[i], playerNum)) :
            result['incorrectSpell'] += 1

        #각 게임의 시간을 gameLengthPerGame에 저장, 11.20패치에서는 단위가 ms였으나 s로 바뀜. 너무 오래 랭겜을 안했으면 값이 이상할 수 있습니다.
        result['gameLengthPerGame'].append( round(getGameLength(matchInfo[i]) / 60,2))

        #와드 설치 갯수를 wardPalcedPerGame에 저장
        result['wardPlacedPerGame'].append(getWardPlaced(matchInfo[i], playerNum))

        #골드 수급량을 goldEarnedPerGame에 저장
        result['goldEarnedPerGame'].append(getHowMuchGoldEarned(matchInfo[i], playerNum))

        #골드 수급량을 goldSpentPerGame에 저장
        result['goldSpentPerGame'].append(getHowMuchGoldSpent(matchInfo[i], playerNum))

        #매 게임의 승패 여부를 weatherWinPerGame에 저장
        result['weatherWinPerGame'].append(getGameWins(matchInfo[i], playerNum))

        #게임에서 사용한 챔피언 이름을 championName에 저장
        result['championNamePerGame'].append(getChampionName(matchInfo[i], playerNum))

    return result