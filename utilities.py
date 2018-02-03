def rotate(l):
    return l[-1:] + l[:-1]

def all_equal(lst):
    return len(set(lst)) == 1

def is_consecutive(lst):
    return len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1

def change_ace_to_one(lst):
    return list(map(lambda x : x if x != 12 else -1, lst))

def most_common(lst):
    return max(set(lst), key=lst.count)