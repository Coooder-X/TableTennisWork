def calSum(arr):
    total = 0
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            total += arr[i][j]
    return total


class TechScoreCase:

    def __init__(self):
        #   strike_ball_sore 表示形如“反手给中路长” 这种，由（身位-落点）确定的击球得分情况，每个元素表示该种击球得分数
        self.strike_ball_score_rec = [[0 for i in range(10)] for i in range(4)]
        self.strike_ball_score_3 = [[0 for i in range(10)] for i in range(4)]
        self.strike_ball_score_4 = [[0 for i in range(10)] for i in range(4)]
        self.strike_ball_score_more = [[0 for i in range(10)] for i in range(4)]

    # def __str__(self):
    #     return ''.join('%s' %id for id in self.strike_ball_score_rec) + ' \n'
    #     + ''.join('%s' %id for id in self.strike_ball_score_3) + ' \n'
    #     + ''.join('%s' %id for id in self.strike_ball_score_4) + ' \n'
    #     + ''.join('%s' %id for id in self.strike_ball_score_more) + ' \n'

    def display(self):
        print(self.strike_ball_score_rec, calSum(self.strike_ball_score_rec))
        print(self.strike_ball_score_3, calSum(self.strike_ball_score_3))
        print(self.strike_ball_score_4, calSum(self.strike_ball_score_4))
        print(self.strike_ball_score_more, calSum(self.strike_ball_score_more))


