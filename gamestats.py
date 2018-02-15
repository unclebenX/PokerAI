import numpy as np
import game as g

"""
MOVING AVERAGE, GRAPHS
"""

class GameStats:    
    def __init__(self, name, big_blind):
        self.name = name
        self.hands_played = 0
        self.hands_won = 0
        self.mean_win = 0
        self.reward = 0
        self.actions = {g.Action.FOLD: 0, g.Action.CHECK: 0, g.Action.BET_CALL: 0}
        self.showdown = 0
        self.showdown_won = 0
        self.win_rate = 0
        self.stack_history = []
        self.big_blind = big_blind
    
    def normalize(self):
        s = sum(self.actions.values())
        for action in self.actions:
            self.actions[action] /= s
        tab = np.diff(np.array(self.stack_history))
        self.mean_win = 0 if len(tab[tab>0])==0 else np.mean(tab[tab>0])/self.big_blind
        
    def display(self):
        print('--- Player: {} ---'.format(self.name))
        print('Hands played     : {}'.format(self.hands_played))
        print('Hands won        : {}%'.format(round(self.hands_won/self.hands_played*100,1)))
        print('Mean win (BB)    : {}'.format(round(self.mean_win,1)))
        print('Reward           : {}'.format(round(self.reward,1)))
        print('Actions          : Fold {}% Check {}% Bet/Call {}%'.format(round(self.actions[g.Action.FOLD]*100), round(self.actions[g.Action.CHECK]*100), round(self.actions[g.Action.BET_CALL]*100)))
        print('Showdowns        : {}%'.format(round(self.showdown/self.hands_played*100,1)))
        if (self.showdown > 0):
            print('Showdowns won    : {}%'.format(round(self.showdown_won/self.showdown*100,0)))
        else:
            print('Showdowns won    : 0%')
        print('Win rate (BB/100): {}'.format(round(self.win_rate,1)))
        