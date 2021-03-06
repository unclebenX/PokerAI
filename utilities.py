import numpy as np
import showdown as sd
import os
import sys

def rotate(l):
    return l[1:] + l[:1]

def all_equal(lst):
    return len(set(lst)) == 1

def is_consecutive(lst):
    return len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1

def change_ace_to_one(lst):
    return list(map(lambda x : x if x != 12 else -1, lst))

def most_common(lst):
    return max(set(lst), key=lst.count)

def sample_distribution_from_dict(dic):
    d_choices = list((dic.keys()))
    d_probs = np.array(list(dic.values()))
    return np.random.choice(d_choices, 1, p=d_probs/sum(d_probs))[0]

def blockPrint():
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    return old_stdout

def enablePrint(old):
    sys.stdout = old
    
def equal_bets(current_bets, remaining_players_hand):
    return all_equal([current_bets[player] for player in remaining_players_hand])

def get_indices(action):
    return action.value - 1

def pack_X(X):
    last_row = X[2].copy()
    last_row.resize((1,13))
    last_row[0,12] = X[3]
    #last_row[0,11] = sd.best_hand(sd.convert_matrix_to_cards(X[0]+X[1]))[0] if np.sum(X[0]+X[1])>=5 else 0.
    feed_input = np.vstack((X[0],X[1], last_row))
    return feed_input.ravel()

get_indices = np.vectorize(get_indices)