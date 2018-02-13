import itertools
import numpy as np
import utilities as u

hands_types = ['High card', 'One pair', 'Two pair', 'Three of a kind', 'Straight',
               'Flush', 'Full house', 'Four of a kind', 'Straight flush', 'Royal flush']

def convert_matrix_to_cards(card_matrix):
    a, cards = np.where(card_matrix==1), []
    for color, value in zip(a[0], a[1]): cards.append((value,color))
    return cards

def evaluate_hand(cards,ranks):
    flush = u.all_equal([c[1] for c in cards])
    if u.is_consecutive(ranks) or u.is_consecutive(u.change_ace_to_one(ranks)):
        if not flush: return 'Straight'
        elif min(ranks) != 8: return 'Straight flush'
        else: return 'Royal flush'
    s = sum(ranks.count(r) for r in ranks)
    if s in [17, 13]:
        return {4 + 4 + 4 + 4 + 1: 'Four of a kind',
                3 + 3 + 3 + 2 + 2: 'Full house'}[s]
    if flush: return 'Flush'
    return {3 + 3 + 3 + 1 + 1: 'Three of a kind',
            2 + 2 + 2 + 2 + 1: 'Two pair',
            2 + 2 + 1 + 1 + 1: 'One pair',
            1 + 1 + 1 + 1 + 1: 'High card'}[s]
        
def hand_score(cards):
    ranks = [c[0] for c in cards]
    hand = evaluate_hand(cards,ranks)
    ranks.sort(reverse=True)
    if hand == 'High card' or hand == 'Flush':
        s = ranks
    elif hand == 'One pair' or hand == 'Three of a kind' or hand == 'Four of a kind':
        card = u.most_common(ranks)
        s = [card] + [r for r in ranks if r != card]
    elif hand == 'Two pair' or hand == 'Full house':
        card1 = u.most_common(ranks)
        card2 = u.most_common([r for r in ranks if r != card1])
        s = [card1, card2] + [r for r in ranks if r != card1 and r != card2]
    elif hand == 'Straight' or hand == 'Straight flush' or hand == 'Royal flush':
        if u.is_consecutive(ranks): s = ranks[0]
        else: s = 5
    return (hands_types.index(hand), s)
    
def best_hand(cards):
    best = max(itertools.combinations(cards, 5), key=hand_score)
    return hand_score(best)

def hand_winners(cards, board):
    board = convert_matrix_to_cards(board)
    winners, max_scores = [], (-1,-1)
    for player in cards.keys():
        s = best_hand(convert_matrix_to_cards(cards[player]) + board)
        if(s>max_scores):
            winners = [player]
            max_scores = s
        elif(s==max_scores):
            winners.append(player)
    return winners