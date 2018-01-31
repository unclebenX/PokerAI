import itertools
import numpy as np
from collections import Counter

hands_types = ['High card',
            'One pair',
            'Two pair',
            'Three of a kind',
            'Straight',
            'Flush',
            'Full house',
            'Four of a kind',
            'Straight flush',
            'Royal flush']

def convert_matrix_to_cards(card_matrix):
    a = np.where(card_matrix==1)
    cards = []
    for color, value in zip(a[0], a[1]):
        cards.append((value,color))
    return cards

def all_equal(lst):
    return len(set(lst)) == 1

def is_consecutive(lst):
    return len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1

def change_ace(lst):
    l = []
    for val in lst:
        l.append((val==12)*(-1)+(val<12)*val)
    return l

def evaluate_hand(cards):
    ranks = [c[0] for c in cards]
    suits = [c[1] for c in cards]
    if is_consecutive(ranks) or is_consecutive(change_ace(ranks)):
        return (
            'Straight' if not all_equal(suits) else
            'Straight flush' if min(ranks) != 10 else
            'Royal flush'
        )
    s = sum(ranks.count(r) for r in ranks)
    if s in [17, 13]:
        return {
            4 + 4 + 4 + 4 + 1: 'Four of a kind',
            3 + 3 + 3 + 2 + 2: 'Full house',
        }[s]
    if all_equal(suits):
        return 'Flush'
    return {
        3 + 3 + 3 + 1 + 1: 'Three of a kind',
        2 + 2 + 2 + 2 + 1: 'Two pair',
        2 + 2 + 1 + 1 + 1: 'One pair',
        1 + 1 + 1 + 1 + 1: 'High card',
    }[s]

def most_common(lst):
    count = Counter(lst)
    return count.most_common(1)[0][0]
        
def hand_score(cards):
    hand = evaluate_hand(cards)
    ranks = list(np.sort([c[0] for c in cards])[::-1])
    if hand == 'High card':
        s = ranks
    elif hand == 'One pair':
        pair = most_common(ranks)
        s = [pair] + [r for r in ranks if r != pair]
    elif hand == 'Two pair':
        pair1 = most_common(ranks)
        pair2 = most_common([r for r in ranks if r != pair1])
        s = [pair1, pair2] + [r for r in ranks if r != pair1 and r != pair2]
    elif hand == 'Three of a kind':
        three = most_common(ranks)
        s = [three] + [r for r in ranks if r != three]
    elif hand == 'Straight' or hand == 'Straight flush' or hand == 'Royal flush':
        if(not is_consecutive(ranks) and is_consecutive(change_ace(ranks))):
            s = 5
        else:
            s = ranks[0]
    elif hand == 'Flush':
        s = ranks
    elif hand == 'Full house':
        three = most_common(ranks)
        pair = most_common([r for r in ranks if r != three])
        s = [three, pair]
    else:
        four = most_common(ranks)
        s = [four] + [r for r in ranks if r != four]
    return (hands_types.index(hand), s)
    
def best_hand(cards):
    best = max(itertools.combinations(cards, 5), key=hand_score)
    return best, hand_score(best)