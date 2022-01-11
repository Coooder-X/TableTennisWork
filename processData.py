import json
import utils
from TechScoreCase import *


def process(fileNameList, callback, isProgress):
    """
    jsonFile = ''
    data = {}
    player1 = ''
    player2 = ''
    playerList = []
    roundList = []
    """
    for fileName in fileNameList:
        print(fileName)
        with open(fileName, 'r', encoding='utf-8') as f:
            jsonFile = f.read()
            jsonFile = json.loads(jsonFile)
            # print(jsonFile)

        data = jsonFile['data']
        playerList = data['player']
        if len(playerList[0]) == 2: #   若是双打数据，报错，返回
            callback()
            return
        player1 = playerList[0][0]['name']
        player2 = playerList[1][0]['name']
        # print(playerList, player1, player2)

        roundList = data['record']['list']  # 若干局，元素是每个个大比分 局内的的信息

        serveList = []
        count = 0

        '''
        scoreCaseDict 用于存储 excel 表右边部分信息，只考虑单打
        运动员的名字为 key，value 是 TechScoreCase 对象，存储 4 个二维矩阵，表示（身位-落点）的线路得分情况
        '''
        scoreCaseDict = {}
        for playerGroup in playerList:
            for player in playerGroup:
                scoreCaseDict[player['name']] = TechScoreCase()

        '''
        lineScoreCaseDict 用于存储 excel 表左部分信息，只考虑单打
        运动员的名字为 key，value 是 一个 dict，存储几个 （身位-落点1-落点2） 线路得分情况
        '''
        lineScoreCaseDict = {}
        for playerGroup in playerList:
            for player in playerGroup:
                lineScoreCaseDict[player['name']] = {}
                for tecType in ['接发球', '第三拍', '第四拍', '相持']:
                    lineScoreCaseDict[player['name']][tecType] = {
                        '反手给斜线': 0,
                        '正手给斜线': 0,
                        '反手给直线': 0,
                        '正手给直线': 0,
                        'total': 0
                    }
        print(lineScoreCaseDict)

        ''' serveDict 用于存储每个运动员的发球轮得分情况
        {
            player1: {
                totalWin: number,
                totalLost: number,
                落点1: {
                    win: number,
                    lost: number    
                },
                ...
            },
            ...
        } 
        '''
        serveDict = {}
        for playerGroup in playerList:
            for player in playerGroup:
                serveDict[player['name']] = {'totalWin': 0, 'totalLost': 0}

        c1 = 0
        c2 = 0
        c3 = 0

        for round in roundList:  # 其中的一局的信息
            pointList = round['list']  # pointList 中元素是该局的每一分的信息
            # print(playerList[utils.getServeSide(pointList[0])][0]['name'])  # 测试判断发球方的函数

            for point in pointList:  # point 记录该分中的信息
                rallyList = point['list']  # rallyList 记录该分中所有挥拍，每个元素是一个挥拍
                serveSide = playerList[utils.getServeSide(point)][0]  # 下标 0 表示一方的第 0 个球员，单打都为0，serveSide 存储运动员对象
                winSide = playerList[point['winSide']][0]
                serve = rallyList[0]
                recServe = rallyList[1]
                # print(recServe)
                servePoint = recServe['BallPosition']['value']  # 该分中发球方的落点
                if winSide['name'] == player1:
                    c1 += 1
                else:
                    c2 += 1
                if len(rallyList) == 2:
                    c3 += 1
                # 根据当前分输赢和发球落点，更新运动员发球得分情况
                utils.updateServeDict(serveDict, servePoint, serveSide, winSide)
                # 根据当前 rally 信息，更新运动员（身位-落点）线路得分情况
                utils.updateScoreCase(scoreCaseDict, rallyList, playerList[0][0], playerList[1][0], serveSide, winSide)
                # 根据当前 rally 信息，更新运动员（身位-落点1-落点2）线路得分情况
                utils.updateLineScoreCase(lineScoreCaseDict, rallyList, playerList[0][0], playerList[1][0],
                                          winSide, rallyList[-2]['index'])
                serveList.append(recServe)

        print(serveDict)
        scoreCaseDict['陈梦'].display()
        print('----------------')
        scoreCaseDict['王曼昱'].display()
        print(lineScoreCaseDict)
        print(c1, c2, c3)
        utils.createExcel(fileName, serveDict, scoreCaseDict, lineScoreCaseDict, [player1, player2])
