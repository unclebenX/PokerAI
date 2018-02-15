import numpy as np

"""
X : (self.cards[player], self.board, stacks, self.pot)
"""

class Player:
    def __init__(self, name):
        self.name = name
    
    def display(self):
        return self.name#'{}, F: {}, C: {}, B/C: {}'.format(self.name, round(self.get_policy([])[0],2), round(self.get_policy([])[1],2), round(self.get_policy([])[2],2))
    
class RandomPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        
    def get_policy(self, X):
        return np.array([1./3,1./3,1./3])
    
class FishPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        
    def get_policy(self, X):
        return np.array([1./6,1./6,2./3])
    
class DegenPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        
    def get_policy(self, X):
        return np.array([0.,0.,1.])

class CleverPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        
    def get_policy(self, X):
        u = np.sum(X[0]+X[1],axis=0)
        if(max(u) > 1 and len(np.where(X[2]>0.015)) < 3):# or u[-3] > 0):
            return np.array([0.,0.,1.])
        else:
            return np.array([1.,0.,0.])
        