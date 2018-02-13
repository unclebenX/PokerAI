import numpy as np

class Deck:
    def __init__(self):
        self.cards = np.ones((4,13))
        return
        
    def get_card(self):
        a = np.where(self.cards==1)
        i = np.random.randint(len(a[0]))
        card = (a[0][i],a[1][i])
        self.cards[card] = 0
        return card
    
    def reset(self):
        self.__init__()
        return