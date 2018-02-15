import game as g
import player as p
import numpy as np
import matplotlib.pyplot as plt
import utilities as u

players = []
players.append(p.CleverPlayer('Clever'))
for i in range(6):
    players.append(p.FishPlayer('Fish'+str(i)))
g = g.Game(players)#,p3])
old = u.blockPrint()
for i in range(1):
    g.play_game(N=100)
    #g.reset_game()
u.enablePrint(old)
for player in players:
    #g.game_stats[player].display()
    plt.plot(g.game_stats[player].stack_history,label=player.name)
    plt.legend()