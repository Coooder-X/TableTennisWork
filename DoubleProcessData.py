import openpyxl
import json
import utils


def process(fileNameList):
    """
    jsonFile = ''
    data = {}
    player1 = ''
    player2 = ''
    playerList = []
    roundList = []
    """
    # fileNameList = ['20210726 东京奥运会 混双决赛 许昕刘诗雯vs水谷隼伊藤美诚-collect_project.json']
    for fileName in fileNameList:
        print(fileName)
        with open(fileName, 'r', encoding='utf-8') as f:
            jsonFile = f.read()
            jsonFile = json.loads(jsonFile)

    data = jsonFile['data']
    playerList = data['player']
    team1 = playerList[0]
    team2 = playerList[1]
    # player1 = playerList[0][0]['name']
    # player2 = playerList[1][0]['name']
    print(playerList, team1, team2)

    roundList = data['record']['list']  # 若干局，元素是每个个大比分 局内的的信息

    serveList = []
    count = 0

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
            utils.getDoublesServeSide(point, playerList)
            # rallyList = point['list']  # rallyList 记录该分中所有挥拍，每个元素是一个挥拍
            # serveSide = playerList[utils.getServeSide(point)][0]  # 下标 0 表示一方的第 0 个球员，单打都为0，serveSide 存储运动员对象
            # winSide = playerList[point['winSide']][0]
            # serve = rallyList[0]
            # recServe = rallyList[1]
            # # print(recServe)
            # servePoint = recServe['BallPosition']['value']  # 该分中发球方的落点

