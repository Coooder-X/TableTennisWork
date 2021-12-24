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


def createDoublesExcel(excelScoreCase, calScore):
    pass


#   carry 双打换发球的情况，第一个if是开局初始化顺序，第二个是局间、决胜局第5分换次序的情况
def updateServeRecOrder(serve_rec_order, serve, rec=''):
    if serve_rec_order['00'] == '': # 第一局第一分的初始化
        serve_rec_order[serve] = rec
        serve_rec_order[rec] = getTeamMate(serve)
        serve_rec_order[getTeamMate(serve)] = getTeamMate(rec)
        serve_rec_order[getTeamMate(rec)] = serve
        return
    if rec == '':
        rec = serve_rec_order[serve]
        serve_rec_order[serve], serve_rec_order[getTeamMate(serve)] = serve_rec_order[getTeamMate(serve)], serve_rec_order[serve]
        serve_rec_order[rec], serve_rec_order[getTeamMate(rec)] = serve_rec_order[getTeamMate(rec)], serve_rec_order[rec]
        # serve_rec_order[serve] = getTeamMate(serve_rec_order[serve])
        # serve_rec_order[rec] = serve
        # serve_rec_order[getTeamMate(serve)] = rec
        # serve_rec_order[getTeamMate(rec)] = getTeamMate(serve)



