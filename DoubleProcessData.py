import os
import excelUtils
import openpyxl
import json
import DoubleUtils
from openpyxl.styles import Alignment, PatternFill, Font


def process(fileNameList, callback):
    serve_rec_order = {'00': '', '01': '', '10': '', '11': ''}
    nowLine = 1
    fileIdx = 0
    exl = openpyxl.Workbook()
    sheet = exl.create_sheet('Sheet1', 0)  # 打开该Excel里对应的sheet
    align = Alignment(horizontal='center', vertical='center')

    # fileNameList = ['20210726 东京奥运会 混双决赛 许昕刘诗雯vs水谷隼伊藤美诚-collect_project.json']
    for fileName in fileNameList:
        fileIdx += 1

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
        count = 0
        # print(DoubleUtils.getHitOrders(playerList))

        for roundId, round in enumerate(roundList):  # 其中的一局的信息
            cnt = 0
            cnt2 = 0

            pointList = round['list']  # pointList 中元素是该局的每一分的信息
            # print(playerList[utils.getServeSide(pointList[0])][0]['name'])  # 测试判断发球方的函数
            for pointId, point in enumerate(pointList):
                count += 1
                rallyList = point['list']  # rallyList 记录该分中所有挥拍，每个元素是一个挥拍
                rallyNum = len(rallyList)

                #   单打情况--------------------------------------------------
                if len(hitOrders) == 2:
                    for index, hitPair in enumerate(hitOrders):
                        # index = hitOrders.index(hitPair)
                        A1, A2 = hitPair[0], hitPair[1]
                        if rallyNum == 1:  # 发球失误的情况特判一下
                            if rallyList[0]['HitPlayer'] == hitPair[0] == A1 and hitPair[1] == B1:
                                cnt2 += 1
                                DoubleUtils.updateScoreCase(scoreCase, index, 0, 0, 'lost')
                            elif rallyList[0]['HitPlayer'] == hitPair[0] == B1 and hitPair[1] == A1:
                                DoubleUtils.updateScoreCase(scoreCase, index, 1, 1, 'win')
                            break
                        servePair = [rallyList[0]['HitPlayer'], rallyList[1]['HitPlayer']]
                        lastHitPair = [rallyList[-2]['HitPlayer'], rallyList[-1]['HitPlayer']]
                        if A1 == servePair[0]:
                            if lastHitPair[0] == A1:
                                DoubleUtils.updateScoreCase(scoreCase, index, 0, rallyNum - 2, 'win')
                            else:
                                DoubleUtils.updateScoreCase(scoreCase, index, 0, rallyNum - 1, 'lost')
                        else:
                            if lastHitPair[0] == A1:
                                DoubleUtils.updateScoreCase(scoreCase, index, 1, rallyNum - 2, 'win')
                            else:
                                DoubleUtils.updateScoreCase(scoreCase, index, 1, rallyNum - 1, 'lost')
                    continue

                #   双打情况--------------------------------------------------
                if roundId == 0 and pointId == 0:
                    DoubleUtils.updateServeRecOrder(serve_rec_order, rallyList[0]['HitPlayer'], rallyList[1]['HitPlayer'])

                if roundId == len(roundList):# 决胜局到5分换发球情况
                    if max(point['score']) == 5 and (point['score'][0] + point['score'][1]) % 2 == 1:
                        DoubleUtils.updateServeRecOrder(serve_rec_order, rallyList[0]['HitPlayer'])

                for index, hitPair in enumerate(hitOrders):
                    # index = hitOrders.index(hitPair)

                    A1 = hitPair[DoubleUtils.getChinaPlayer(hitPair, playerList)]  # 当前pair中中国运动员
                    B1 = hitPair[DoubleUtils.getOppositePlayer(hitPair, playerList)]  # 当前pair对方运动员

                    if rallyNum == 1:  # 发球失误的情况特判一下
                        pair = [rallyList[0]['HitPlayer'], serve_rec_order[rallyList[0]['HitPlayer']]]
                        idx = hitOrders.index(pair)
                        print('发球失误', hitPair, cnt, ':', cnt2)
                        if pair[0] == A1:
                            cnt2 += 1
                            DoubleUtils.updateScoreCase(scoreCase, idx, 0, 0, 'lost')
                        elif pair[0] == B1:
                            print('对方发球失误')
                            print(pair)
                            cnt += 1
                            DoubleUtils.updateScoreCase(scoreCase, idx, 1, 1, 'win')
                        break

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
        print('total point = ', count)

        excelScoreCase = {}
        calScore = {}
        count = 0
        MaxScore = 0
        for i in range(len(scoreCase)):
            # print(hitOrders[i])
            p1 = DoubleUtils.getPlayerName(hitOrders[i][0], playerList)
            p2 = DoubleUtils.getPlayerName(hitOrders[i][1], playerList)
            case = p1 + '→' + p2
            case2 = case
            excelScoreCase[case] = {0: {}, 1: {}}
            if len(hitOrders) == 8: #   区分单、双打情况的输出
                p3 = DoubleUtils.getPlayerName(DoubleUtils.getTeamMate(hitOrders[i][0]), playerList)
                p4 = DoubleUtils.getPlayerName(DoubleUtils.getTeamMate(hitOrders[i][1]), playerList)
                case2 += '→' + p3 + '→' + p4
            calScore[case2] = {'得分数': 0, '失分数': 0, '得分率': 0, '优劣势': ''}
            win = 0
            lost = 0
            for j in range(2):
                #-------------这段代码用于把某情况的最大拍数以内补齐，即没数据的补0。若还不足3列，则补到3列
                maxShoot = max(scoreCase[i][j].keys())
                tmp = maxShoot
                # print('scoreCase[i][j]', scoreCase[i][j], maxShoot)
                while tmp >= 0:
                    if tmp not in scoreCase[i][j].keys():
                        scoreCase[i][j][tmp] = {'win': 0, 'lost': 0}
                        # print('add')
                    tmp -= 4
                while len(scoreCase[i][j].keys()) < 3:
                    maxShoot += 4
                    scoreCase[i][j][maxShoot] = {'win': 0, 'lost': 0}
                #---------------
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
                    MaxScore = max(MaxScore, scoreCase[i][j][key]['win'], scoreCase[i][j][key]['lost'])
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

        # sheet.merge_cells('A%s:N%s' % (str(fileIdx), str(fileIdx)))
        for pair in excelScoreCase.keys():
            sheet.cell(nowLine, 1, os.path.split(fileName)[1].split('.')[0] + '   ' + pair).alignment = align
            sheet.cell(nowLine, 1).font = Font(bold=True)
            sheet.merge_cells(start_row=nowLine, start_column=1, end_row=nowLine, end_column=14)

            doubleLine = excelScoreCase[pair]
            for i in range(2):
                line = doubleLine[i]
                shoots = list(line.keys())
                for j in range(len(shoots)):
                    sheet.cell(nowLine+1+i*3, j*2+1, shoots[j]).alignment = align
                    sheet.merge_cells(start_row=nowLine+1+i*3, start_column=j*2+1, end_row=nowLine+1+i*3, end_column=j*2+2)
                    sheet.cell(nowLine + 2 + i * 3, j * 2 + 1, '得分').alignment = align
                    sheet.cell(nowLine + 2 + i * 3+1, j * 2 + 1, line[shoots[j]]['win']).alignment = align
                    excelUtils.fillColorByValue(MaxScore, line[shoots[j]]['win'], sheet, nowLine + 2 + i * 3+1, j * 2 + 1, 0)
                    sheet.cell(nowLine + 2 + i * 3, j * 2 + 2, '失分').alignment = align
                    sheet.cell(nowLine + 2 + i * 3+1, j * 2 + 2, line[shoots[j]]['lost']).alignment = align
                    excelUtils.fillColorByValue(MaxScore, line[shoots[j]]['lost'], sheet, nowLine + 2 + i * 3+1, j * 2 + 2, 1)

            nowLine += 7

        nowLine += 1
        fillRed = PatternFill("solid", fgColor="f89588")
        fillRGreen = PatternFill("solid", fgColor="76da91")

        sheet.cell(nowLine, 1, '发接发顺序').alignment = align
        sheet.cell(nowLine, 1).font = Font(bold=True)
        sheet.merge_cells(start_row=nowLine, start_column=1, end_row=nowLine, end_column=4)

        order = list(calScore.keys())
        sheet.cell(nowLine, 1, '发接发顺序').alignment = align
        sheet.cell(nowLine, 5, '得分数').alignment = align
        sheet.cell(nowLine, 6, '失分数').alignment = align
        sheet.cell(nowLine, 7, '得分率').alignment = align
        sheet.cell(nowLine, 8, '优劣势').alignment = align
        sheet.cell(nowLine, 1).font = Font(bold=True)
        sheet.cell(nowLine, 5).font = Font(bold=True)
        sheet.cell(nowLine, 6).font = Font(bold=True)
        sheet.cell(nowLine, 7).font = Font(bold=True)
        sheet.cell(nowLine, 8).font = Font(bold=True)
        nowLine += 1
        for i in range(len(order)):
            sheet.cell(nowLine, 1, order[i]).alignment = align
            sheet.merge_cells(start_row=nowLine, start_column=1, end_row=nowLine, end_column=4)
            sheet.cell(nowLine, 5, calScore[order[i]]['得分数']).alignment = align
            sheet.cell(nowLine, 6, calScore[order[i]]['失分数']).alignment = align
            sheet.cell(nowLine, 7, calScore[order[i]]['得分率']).alignment = align
            sheet.cell(nowLine, 8, calScore[order[i]]['优劣势']).alignment = align
            if calScore[order[i]]['优劣势'] == '劣势':
                sheet.cell(nowLine, 8).fill = fillRed
            elif calScore[order[i]]['优劣势'] == '优势':
                sheet.cell(nowLine, 8).fill = fillRGreen

            nowLine += 1
        nowLine += 1

    exl.save('双打得失分数据统计（共' + str(fileIdx) + '场比赛）' + '.xlsx')
