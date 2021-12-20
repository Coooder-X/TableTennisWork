import openpyxl
import json
import DoubleUtils


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
    print(playerList, team1, team2)

    roundList = data['record']['list']  # 若干局，元素是每个个大比分 局内的的信息

    hitOrders = DoubleUtils.getHitOrders(playerList)
    print(hitOrders)
    # scoreCase在双打时有8个元素，每个元素是一个[]， 里面有2个dict，分别是2种开球情况，dict里面第x个元素存放第x拍的得失分{'win': 0, 'lose': 0}
    scoreCase = [[{}, {}] for i in range(len(hitOrders))]
    print(scoreCase)

    c1 = 0
    c2 = 0
    c3 = 0
    # print(DoubleUtils.getHitOrders(playerList))

    for round in roundList:  # 其中的一局的信息
        cnt = 0
        cnt2 = 0

        pointList = round['list']  # pointList 中元素是该局的每一分的信息
        # print(playerList[utils.getServeSide(pointList[0])][0]['name'])  # 测试判断发球方的函数
        for point in pointList:
            rallyList = point['list']  # rallyList 记录该分中所有挥拍，每个元素是一个挥拍
            rallyNum = len(rallyList)

            for hitPair in hitOrders:
                index = hitOrders.index(hitPair)

                A1 = hitPair[DoubleUtils.getChinaPlayer(hitPair, playerList)]  # 当前pair中中国运动员
                B1 = hitPair[DoubleUtils.getOppositePlayer(hitPair, playerList)]  # 当前pair对方运动员

                if rallyNum == 1:  # 发球失误的情况特判一下/////////////////////////////////////////////////////
                    if rallyList[-1] == hitPair[0] == A1:
                        DoubleUtils.updateScoreCase(scoreCase, index, 0, 0, 'lost')
                    continue

                servePair = [rallyList[0]['HitPlayer'], rallyList[1]['HitPlayer']]
                lastHitPair = [rallyList[-2]['HitPlayer'], rallyList[-1]['HitPlayer']]
                # 满足A1->B1的模式，计算A1给B1赢的情况，分2种：A1发球和A2发球
                if servePair[0][0] == A1[0] and hitPair[0][0] == A1[0]:  # 必须要满足A发球并且hitPair也是A在前，否则会出现拍数归类错误
                    if hitPair == lastHitPair and A1 == hitPair[0]:
                        # if servePair[0][0] == A1[0]:
                        if servePair[0] == A1:
                            cnt += 1
                            DoubleUtils.updateScoreCase(scoreCase, index, 0, rallyNum - 2, 'win')
                            break
                        else:
                            cnt += 1
                            DoubleUtils.updateScoreCase(scoreCase, index, 1, rallyNum - 2, 'win')
                            break
                    # 满足A1->B1的模式，计算A1给B1输的情况，分2种：A1发球和A2发球，最后一rally是B2->A1
                    elif lastHitPair[0] != B1 and lastHitPair[1] == A1:
                        # if servePair[0][0] == A1[0]:
                        if servePair[0] == A1:
                            cnt2 += 1
                            DoubleUtils.updateScoreCase(scoreCase, index, 0, rallyNum - 1, 'lost')
                            break
                        else:
                            cnt2 += 1
                            DoubleUtils.updateScoreCase(scoreCase, index, 1, rallyNum - 1, 'lost')
                            break

                elif servePair[0][0] == B1[0] and hitPair[0][0] == B1[0]:
                    # 满足B1->A1的模式，计算B1给A1赢（A1输）的情况，分2种：B1发球和B2发球
                    if lastHitPair == hitPair and hitPair[0] == B1:
                        # if servePair[0][0] == B1[0]:
                        if servePair[0] == B1:
                            cnt2 += 1
                            DoubleUtils.updateScoreCase(scoreCase, index, 0, rallyNum - 1, 'lost')
                            break
                        else:
                            cnt2 += 1
                            DoubleUtils.updateScoreCase(scoreCase, index, 1, rallyNum - 1, 'lost')
                            break
                    # 满足B1->A1的模式，计算B1给A1输（A1赢）的情况，分2种：B1发球和B2发球，最后一rally是A1->B2
                    elif lastHitPair[0] == A1 and lastHitPair[1] != B1:
                        # if servePair[0][0] == B1[0]:
                        if servePair[0] == B1:
                            cnt += 1
                            DoubleUtils.updateScoreCase(scoreCase, index, 0, rallyNum - 2, 'win')
                            break
                        else:
                            cnt += 1
                            DoubleUtils.updateScoreCase(scoreCase, index, 1, rallyNum - 2, 'win')
                            break
        print(cnt, cnt2)

    print(scoreCase)

    excelScoreCase = {}
    calScore = {}
    count = 0
    for i in range(len(scoreCase)):
        # print(hitOrders[i])
        p1 = DoubleUtils.getPlayerName(hitOrders[i][0], playerList)
        p2 = DoubleUtils.getPlayerName(hitOrders[i][1], playerList)
        case = p1 + '→' + p2
        excelScoreCase[case] = {0: {}, 1: {}}
        p3 = DoubleUtils.getPlayerName(DoubleUtils.getTeamMate(hitOrders[i][0]), playerList)
        p4 = DoubleUtils.getPlayerName(DoubleUtils.getTeamMate(hitOrders[i][1]), playerList)
        case2 = case + '→' + p3 + '→' + p4;
        calScore[case2] = {'得分数': 0, '失分数': 0, '得分率': 0, '优劣势': ''}
        win = 0
        lost = 0
        for j in range(2):
            for key in sorted(scoreCase[i][j]):
                if key == 0:
                    shoot = '发球'
                elif key == 1:
                    shoot = '接发球'
                else:
                    shoot = '第' + str(key + 1) + '拍'
                excelScoreCase[case][j][shoot] = scoreCase[i][j][key]
                win += scoreCase[i][j][key]['win']
                lost += scoreCase[i][j][key]['lost']
                count += scoreCase[i][j][key]['win'] + scoreCase[i][j][key]['lost']
        calScore[case2]['得分数'] = win
        calScore[case2]['失分数'] = lost
        rate = float(win * 100) / float(win + lost)
        calScore[case2]['得分率'] = format(rate, '.1f') + '%'
        if rate > 50:
            calScore[case2]['优劣势'] = '优势'
        elif rate == 50:
            calScore[case2]['优劣势'] = '均势'
        else:
            calScore[case2]['优劣势'] = '劣势'

    print(excelScoreCase)
    print(calScore)

    for i in excelScoreCase.keys():
        print(i)
        print('A', excelScoreCase[i][0])
        print('B', excelScoreCase[i][1])
        print('---------------------------------------')
    print(count)
