# 返回本 point 发球的 player 对象
def getDoublesServeSide(point, playerList):
    rallyList = point['list']
    serveStr = rallyList[0]['HitPlayer']
    teamID, playerID = int(serveStr[0]), int(serveStr[1])
    # print(playerList[teamID][playerID]['name'])
    return playerList[teamID][playerID]