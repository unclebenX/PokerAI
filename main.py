import game as g
import player as p
import numpy as np
import matplotlib.pyplot as plt
import utilities as u

p1, p2, p3 = p.CleverPlayer('Clever'), p.CleverPlayer('Clever2'), p.CleverPlayer('Clever3')#, p.RandomPlayer('Random')
players = [p1,p2,p3]
stats_final = {p1:0,p2:0,p3:0}
nb_vic = {p1:0, p2:0,p3:0}
stats_history = {p1:[],p2:[],p3:[]}
g = g.Game([p1,p2,p3])
#old = u.blockPrint()
for i in range(1):
    s = g.play_game(N=1000)
    for player in s[0].keys():
        stats_final[player] += s[1][player]
    win = max(s[1], key=s[1].get)
    nb_vic[win] += 1
    g.reset_game()
#u.enablePrint(old)
stats_history = s[0]
plt.clf()
for pl in players:
    plt.plot(stats_history[pl], label=pl.display())
plt.show()
