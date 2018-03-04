import game as g
import player as p
import numpy as np
import matplotlib.pyplot as plt
import utilities as u

players = []
players.append(p.CleverPlayer('Clever'))
players.append(p.CleverPlayer('Clever2'))
g = g.Game(players)
#old = u.blockPrint()
data = g.play_game(N=1000)
#u.enablePrint(old)
#for player in players:
#    #g.game_stats[player].display()
#    plt.plot(g.game_stats[player].stack_history,label=player.name)
#    plt.legend()
#g.game_stats[players[0]].display()