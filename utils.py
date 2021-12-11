# 判断发球方，返回运动员下标
def getServeSide(point):
    if point['startSide'] != -1:
        return point['startSide']
    winSide = point['winSide']
    rallyNum = len(point['list'])
    # 偶数拍发球方win，奇数拍发球方lost
    if rallyNum % 2 == 0:
        serveSide = winSide
    else:
        serveSide = 1 if winSide == 0 else 0
    return serveSide


# 根据当前 发球落点、发球方、该point数据，推断发球方胜负，并更新 dict
def updateServeDict(serveDict, servePoint, serveSide, winSide):
    if not (servePoint in serveDict[serveSide['name']]):
        serveDict[serveSide['name']][servePoint] = {'win': 0, 'lost': 0}
    if winSide['name'] == serveSide['name']:
        serveDict[serveSide['name']][servePoint]['win'] += 1
        serveDict[serveSide['name']]['totalWin'] += 1
    else:
        serveDict[serveSide['name']][servePoint]['lost'] += 1
        serveDict[serveSide['name']]['totalLost'] += 1


#   判断 player1 的击球是斜线还是直线 diagonal | straight
 #  strikePos 是 p1 挥拍的身位，point1 是 p1 接到的球的落点，point2 是 p1 打到 p2 桌上的落点
def getStrokeDir(strikePos, point1, point2, player1, player2):
    straight = 'straight'
    diagonal = 'diagonal'
    backhand = 'B'
    forehand = 'F'
    reBackhand = 'T'
    reForehand = 'P'
    if player1['rightHand'] == player2['rightHand']:    # 执拍手相同，不需要判断
        if strikePos == backhand:
            if (point1[0] == 'B' == point2[0]) or (point1[0] == 'M' and point2[0] == 'B'):
                return [backhand, diagonal]
            if (point1[0] == 'B' and point2[0] == 'F') or (point1[0] == 'B' and point2[0] == 'M')\
                    or (point1[0] == 'M' and point2[0] == 'F') or (point1[0] == point2[0] == 'M'):
                return [backhand, straight]
        elif strikePos == forehand:
            if (point1[0] == 'F' == point2[0]) or (point1[0] == 'M' and point2[0] == 'F')\
                    or (point1[0] == 'M' and point2[0] == 'B'):
                return [forehand, diagonal]
            if (point1[0] == 'F' and point2[0] == 'M') or (point1[0] == 'F' and point2[0] == 'B')\
                    or ([point1[0] == 'M' == point2[0]]):
                return [forehand, straight]
        elif strikePos == reBackhand:
            if (point1[0] == 'B' and point2[0] == 'F') or (point1[0] == 'M' and point2[0] == 'B'):
                return [backhand, diagonal]
            if (point1[0] == 'F' and point2[0] == 'M') or (point1[0] == 'F' and point2[0] == 'B'):
                return [backhand, straight]
        elif strikePos == reForehand:
            if (point1[0] == 'B' == point2[0]) or (point1[0] == 'M' and point2[0] != 'M'):
                return [forehand, diagonal]
            if (point1[0] == 'B' and point2[0] == 'F') or (point1[0] == 'B' and point2[0] == 'M'):
                return [forehand, straight]
    else:   #   执拍手不同，需要判断一下
        if strikePos == backhand:
            if (point1[0] == 'B' and point2[0] == 'F') or (point1[0] == 'M' and point2[0] == 'F'):
                return [backhand, diagonal]
            if (point1[0] == 'B' and point2[0] == 'B') or (point1[0] == 'B' and point2[0] == 'M') \
                    or (point1[0] == 'M' and point2[0] == 'B') or (point1[0] == point2[0] == 'M'):
                return [backhand, straight]
        elif strikePos == forehand:
            if (point1[0] == 'F' and point2[0] == 'B') or (point1[0] == 'M' and point2[0] == 'F') \
                    or (point1[0] == 'M' and point2[0] == 'B'):
                return [forehand, diagonal]
            if (point1[0] == 'F' and point2[0] == 'M') or (point1[0] == 'F' and point2[0] == 'F') \
                    or ([point1[0] == 'M' == point2[0]]):
                return [forehand, straight]
        elif strikePos == reBackhand:
            if (point1[0] == 'B' and point2[0] == 'B') or (point1[0] == 'M' and point2[0] == 'F'):
                return [backhand, diagonal]
            if (point1[0] == 'F' and point2[0] == 'M') or (point1[0] == 'F' and point2[0] == 'F'):
                return [backhand, straight]
        elif strikePos == reForehand:
            if (point1[0] == 'B' and point2[0] == 'F') or (point1[0] == 'M' and point2[0] != 'M'):
                return [forehand, diagonal]
            if (point1[0] == 'B' and point2[0] == 'B') or (point1[0] == 'B' and point2[0] == 'M'):
                return [forehand, straight]
'''
        if point1[0] == point2[0]:
            if point1[0] == point2[0] == 'F':
                return diagonal
            if point1[0] == point2[0] == 'B':
                return diagonal
            if point1[0] == point2[0] == 'M':
                return straight
        else:
            if point1[0] == 'F':
                if point2[0] == 'B':
                    return straight
                else:
                    return diagonal
            elif point1[0] == 'B':
                if point2[0] == 'F':
                    return straight
                else:
                    return diagonal
            else:   # point1[0] == 'M'
                return diagonal
    else:   #   执拍手不同，需要判断一下斜线
        if point1[0] == point2[0]:
            if point1[0] == point2[0] == 'F':
                return straight
            if point1[0] == point2[0] == 'B':
                return straight
            if point1[0] == point2[0] == 'M':
                return straight
        else:
            if point1[0] == 'F':
                if point2[0] == 'B':
                    return diagonal
                else:
                    return straight
            elif point1[0] == 'B':
                if point2[0] == 'F':
                    return diagonal
                else:
                    return straight
            else:  # point1[0] == 'M'
                return diagonal
'''

# 根据 rallyList、最后一拍之间的2个球员、得分球员，推断获胜方是用什么线路赢球的，例如“反手给斜线”，并更新 dict
def updateStrokeDict(rallyList, player1, player2, winSide):
    winStroke = rallyList[-2]
    lastStroke = rallyList[-1]
    winIndex = winStroke['index']   # 获胜方的最后一击是第几拍
    # 反手给斜线 Back_2_Diagonal
    dirction = getStrokeDir(winStroke['BallPosition']['value'], lastStroke['BallPosition']['value'], player1, player2)  # 获胜方最后一击的击球方向
    winBody = winStroke['StrikePosition']['value']  # 获胜方最后一击的身位
    if winBody == 'S1':
        pass
    elif winBody == 'S2':
        pass
    elif winBody == 'F':
        pass
    elif winBody == 'B':
        pass
    elif winBody == 'T':
        pass
    elif winBody == 'P':
        pass


def updateScoreCase(scoreCaseDict, rallyList, player1, player2, serveSide, winSide):
    #   mp 前4个表示身位字符值对应的矩阵行号，后9个表示落点字符值对应的矩阵列号，整个mp用于根据字符值映射二维矩阵下标
    mp = {'B': 0, 'F': 1, 'P': 2, 'T': 3, 'BS': 0, 'BH': 1, 'BL': 2, 'MS': 3, 'MH': 4, 'ML': 5, 'FS': 6,
          'FH': 7, 'FL': 8, 'SP': 9}
    winStroke = rallyList[-2]
    lastStroke = rallyList[-1]
    winStrike = winStroke['StrikePosition']['value']
    winBallPos = lastStroke['BallPosition']['value']
    # if player1['rightHand'] == player2['rightHand']:  # 执拍手相同
    # 赢的一方的最后一拍是相持阶段的，那么 scoreCaseDict 中获胜方运动员的相持得分中，对应的（身位-落点）线路得分 +1
    if winStroke['index'] > 3:  # 双方击球大于4板认为是相持
        scoreCaseDict[winSide['name']].strike_ball_score_more[mp[winStrike]][mp[winBallPos]] += 1
    if winStroke['index'] == 3:  # 第4拍得分情况
        scoreCaseDict[winSide['name']].strike_ball_score_4[mp[winStrike]][mp[winBallPos]] += 1
    if winStroke['index'] == 2:  # 第3拍得分情况
        scoreCaseDict[winSide['name']].strike_ball_score_3[mp[winStrike]][mp[winBallPos]] += 1
    if winStroke['index'] == 1:  # 接发球得分情况
        scoreCaseDict[winSide['name']].strike_ball_score_rec[mp[winStrike]][mp[winBallPos]] += 1
    # else:
    #     if winStroke['index'] > 3:  # 双方击球大于4板认为是相持
    #         scoreCaseDict[winSide['name']].strike_ball_score_more[mp[winStrike]][mp[winBallPos]] += 1
    #     if winStroke['index'] == 3:  # 第4拍得分情况
    #         scoreCaseDict[winSide['name']].strike_ball_score_4[mp[winStrike]][mp[winBallPos]] += 1
    #     if winStroke['index'] == 2:  # 第3拍得分情况
    #         scoreCaseDict[winSide['name']].strike_ball_score_3[mp[winStrike]][mp[winBallPos]] += 1
    #     if winStroke['index'] == 1:  # 接发球得分情况
    #         scoreCaseDict[winSide['name']].strike_ball_rec[mp[winStrike]][mp[winBallPos]] += 1


def updateLineScoreCase(lineScoreCaseDict, rallyList, player1, player2, serveSide, winSide):
    winStroke = rallyList[-2]
    lastStroke = rallyList[-1]
    winStrike = winStroke['StrikePosition']['value']
    point1 = winStroke['BallPosition']['value']
    point2 = lastStroke['BallPosition']['value']
    lineDir = getStrokeDir(winStrike, point1, point2, player1, player2)
    # print(lineDir)
    if lineDir is not None:
        if lineDir[0] == 'B' and lineDir[1] == 'diagonal':
            lineScoreCaseDict[winSide['name']]['反手给斜线'] += 1
        if lineDir[0] == 'F' and lineDir[1] == 'diagonal':
            lineScoreCaseDict[winSide['name']]['正手给斜线'] += 1
        if lineDir[0] == 'B' and lineDir[1] == 'straight':
            lineScoreCaseDict[winSide['name']]['反手给直线'] += 1
        if lineDir[0] == 'F' and lineDir[1] == 'straight':
            lineScoreCaseDict[winSide['name']]['正手给直线'] += 1
    lineScoreCaseDict[winSide['name']]['total'] += 1

