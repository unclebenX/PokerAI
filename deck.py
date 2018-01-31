import numpy as np
import showdown as s

class Deck:
    def __init__(self):
        self.cards = np.ones((4,13))
        
    def get_card(self):
        a = np.where(self.cards==1)
        i = np.random.randint(len(a[0]))
        card = (a[0][i],a[1][i])
        self.cards[card] = 0
        return card
    
    def reset(self):
        self.cards = np.ones((4,13))
    
#for k in range(1000):       
#    d = Deck()
#    board = np.zeros((4,13))
#    for i in range(7):
#        board[d.get_card()]=1
#    cards = s.convert_matrix_to_cards(board)
#    b=s.best_hand(cards)
#    print(cards)
#    print('Cards: {}, Best hand: {}, Score: {}'.format(b[0],s.hands_types[b[1][0]],b[1][1]))