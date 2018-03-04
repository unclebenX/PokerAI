# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 21:40:38 2018

@author: petit
"""

import game as g
import player as p
from AI import AIPlayer
import numpy as np
import matplotlib.pyplot as plt
import utilities as u

players = []
AI_player = AIPlayer('AI')
players.append(AI_player)
players.append(p.CleverPlayer('Clever'))
players.append(p.CleverPlayer('Clever2'))

g = g.Game(players)
mean_rewards = []

for epoch in range(100):
    old = u.blockPrint()
    g.play_game(N=10)
    data_AI = g.training_data[AI_player]
    states, actions, rewards = zip(*data_AI)
    states = [u.pack_X(state) for state in states]
    u.enablePrint(old)
    AI_player.train(states, actions, rewards)
    print('----- Epoch ' + str(epoch) + ' -----')
    g.game_stats[AI_player].display()
    mean_rewards.append(np.mean(rewards))
    g.reset_game()
    print()
    
plt.plot(mean_rewards)