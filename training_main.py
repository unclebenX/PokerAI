# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 21:40:38 2018

@author: petit
"""

import game as g
import player as p
from AI import AIPlayer
from degen_AI import DegenAIPlayer
from baseline_AI import BaselineAIPlayer
from DQN_AI import DQNPlayer
import numpy as np
import matplotlib.pyplot as plt
import utilities as u
import pandas as pd

'''
players = []
DegenAI_player = DegenAIPlayer('AI')
players.append(DegenAI_player)
players.append(p.DegenPlayer('Degen'))

g_degen = g.Game(players)

for epoch in range(1,25000):
    old = u.blockPrint()
    g_degen.play_game(N=100)
    data_AI = g_degen.training_data[DegenAI_player]
    states, actions, rewards = zip(*data_AI)
    states = [u.pack_X(state) for state in states]
    u.enablePrint(old)
    DegenAI_player.train(states, actions, rewards)
    print('----- Epoch ' + str(epoch) + ' -----')
    g_degen.reset_game()
'''

players = []
AI_player = AIPlayer('AI')
players.append(AI_player)
players.append(p.FishPlayer('Fisch'))

g = g.Game(players)
mean_rewards = []

for epoch in range(1,100):
    old = u.blockPrint()
    g.play_game(N=100)
    data_AI = g.training_data[AI_player]
    states, actions, rewards = zip(*data_AI)
    states = [u.pack_X(state) for state in states]
    u.enablePrint(old)
    AI_player.train(states, actions, rewards)
    print('----- Epoch ' + str(epoch) + ' -----')
    g.game_stats[AI_player].display()
    mean_rewards.append(np.mean(rewards))
    g.reset_game()
    #AI_player.exploration_probability *= epoch/(epoch+1)
    print()

plt.figure(1)
plt.clf()
ax = plt.subplot(211)
plt.plot(mean_rewards)
plt.subplot(212, sharex=ax)
plt.plot(pd.Series(mean_rewards).ewm(halflife=20).mean())