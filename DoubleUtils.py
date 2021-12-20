# 返回本 point 发球的 player 对象
def getDoublesServeSide(point, playerList):
    rallyList = point['list']
    serveStr = rallyList[0]['HitPlayer']
    teamID, playerID = int(serveStr[0]), int(serveStr[1])
    # print(playerList[teamID][playerID]['name'])
    return playerList[teamID][playerID]


def getPlayerName(pair, playerList):
    teamID, playerID = int(pair[0]), int(pair[1])
    return playerList[teamID][playerID]['name']


def judgeIsDouble(playerList):
    if len(playerList[0]) == 2:
        return True
    return False


def getHitOrders(playerList):
    orderList = []
    if judgeIsDouble(playerList):
        playerIDList = ['00', '01', '10', '11']
        for i in range(2):
            for j in range(2, 4):
                orderList.append([playerIDList[i], playerIDList[j]])
                orderList.append([playerIDList[j], playerIDList[i]])
    else:
        orderList = [['00', '10'], ['10', '00']]
    # print(orderList.index(['10', '00']))
    return orderList


def getChinaPlayer(hitPair, playerList):
    for i in range(2):
        teamID, playerID = int(hitPair[i][0]), int(hitPair[i][1])
        if playerList[teamID][playerID]['country'] == '中国':
            return i
    return -1


def getOppositePlayer(hitPair, playerList):
    for i in range(2):
        teamID, playerID = int(hitPair[i][0]), int(hitPair[i][1])
        if playerList[teamID][playerID]['country'] != '中国':
            return i
    return -1


def updateScoreCase(scoreCase, index, beginType, num, res):
    if num not in scoreCase[index][beginType].keys():
        scoreCase[index][beginType][num] = {'win': 0, 'lost': 0}
    scoreCase[index][beginType][num][res] += 1


def getTeamMate(playerID):
    res = playerID[0]
    res += '0' if playerID[1] == '1' else '1'
    return res
