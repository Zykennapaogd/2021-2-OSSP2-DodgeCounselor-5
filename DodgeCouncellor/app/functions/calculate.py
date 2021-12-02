from requests.models import HTTPError
from riotwatcher import LolWatcher
from riotwatcher._apis.league_of_legends.SummonerApiV4 import SummonerApiV4
from riotwatcher._apis.league_of_legends.MatchApiV5 import MatchApiV5
import app.functions.functions as fun

DeathKingScore = 5
NoItemScore = 3
BadSpellScore = 2
DamageDiffWeight = 1.0
GoldDiffWeight = 2.0
visionScoreWeight = 2.0

def calculateScorePerUser(userName) :
    summonerDTO = fun.getSummonerInfo(userName)
    matchList = fun.getMatchBySummonerDTO(summonerDTO, 20)
    matchInfos = fun.getMatchInfoByMatchID(matchList)
    print("호출 끝")

    resultSet = {
        "deathKingCount" : 0,
        "badItemCount" : 0,
        "badSpellCount" : 0,
        "weakDamageCount" : 0,
        "lackGoldCount" : 0,
        "visionLowCount" : 0,
        "trollScore" : []
    }

    for i in range(len(matchInfos)) :
        print((i+1), "번째 판 ")
        #처음에 0점짜리 추가
        resultSet['trollScore'].append(0)

        userLoc = fun.getUserLoc(matchInfos[i], summonerDTO['name'])

        #DeathKing의 가중치는 5점
        if (fun.DeathKing(matchInfos[i], userLoc)) :
            resultSet['trollScore'][i] += DeathKingScore
            resultSet['deathKingCount'] += 1

        #noItem의 가중치는 3점
        if (fun.buySameItems(matchInfos[i], userLoc)) :
            resultSet['trollScore'][i] += NoItemScore
            resultSet['badItemCount'] += 1

        if (not(fun.UseCorrectSpell(matchInfos[i], userLoc))) :
            resultSet['trollScore'][i] += BadSpellScore
            resultSet['badSpellCount'] += 1
        
        damageDiff = fun.damageDiffByPosition(matchInfos[i], userLoc)
        if (damageDiff != 0) :
            resultSet['trollScore'][i] += (damageDiff * DamageDiffWeight)
            resultSet['weakDamageCount'] += 1

        goldDiff = fun.goldDiffByPostion(matchInfos[i], userLoc)
        if (goldDiff != 0) :
            resultSet['trollScore'][i] += (goldDiff * GoldDiffWeight)
            resultSet['lackGoldCount'] += 1

        visionDiff = fun.visionScoreDiffByPosition(matchInfos[i], userLoc)
        if (visionDiff != 0) :
            resultSet['trollScore'][i] += (visionDiff * visionScoreWeight)
            resultSet['visionLowCount'] += 1

    return resultSet
