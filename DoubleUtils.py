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


# 返回一个长度为2的列表，第一个元素表示作为统计的对象的队伍ID，第二个是对方的队伍ID
# 如果一支中国一支国外，中国为统计对象，若两支中国或两支国外，选第一个
# 注意返回的是字符串代表队伍类型
def getTargetTeamID(playerList):
    cnt = 0
    res = 0
    for idx in range(2):
        team = playerList[idx]
        player = team[0]
        print(player)
        if player['country'] == '中国':
            cnt += 1
            res = idx
    if cnt == 1:
        return [str(res), '0' if res == 1 else '1']
    else:  # cnt == 0 or cnt == 2:
        return ['0', '1']


# hitPair是形如 ['00', '10'] 的运动员编号对，本函数返回的是中国运动员在本列表中的下标
def getTargetPlayer(hitPair, targetTeamID):
    for i in range(2):
        if hitPair[i][0] == targetTeamID:
            return i


def getOppositePlayer(hitPair, targetTeamID):
    for i in range(2):
        if hitPair[i][0] != targetTeamID:
            return i


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
    if serve_rec_order['00'] == '':  # 第一局第一分的初始化
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
