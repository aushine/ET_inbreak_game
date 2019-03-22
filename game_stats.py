class GameStats():
    '''跟踪游戏的统计信息'''
    def __init__(self, ai_settings):
        '''初始化统计信息'''
        self.ai_settings = ai_settings
        self.reset_stats()
        #游戏刚启动处于活动状态
        self.game_active = False

        with open(r'high_score.txt', 'r') as f:
            self.history_high_score = int(f.readline())
            self.high_score = self.history_high_score
    def highest_score(self):
        if self.high_score > self.history_high_score:
            with open(r'high_score.txt', 'w') as d:
                d.write(str(self.high_score))
    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1