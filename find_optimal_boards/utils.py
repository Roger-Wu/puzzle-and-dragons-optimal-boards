# import operator as op
# from scipy.misc import comb, factorial
# from sympy.utilities.iterables import multiset_permutations


def comb(n, r):
    r = min(r, n-r)
    res = 1
    for i in range(r):
        res *= (n - i)
        res //= (i + 1)
    return res

class unique_element:
    def __init__(self,value,occurrences):
        self.value = value
        self.occurrences = occurrences

def perm_unique(elements):
    eset=set(elements)
    listunique = [unique_element(i,elements.count(i)) for i in eset]
    u=len(elements)
    return perm_unique_helper(listunique,[0]*u,u-1)

def perm_unique_helper(listunique,result_list,d):
    if d < 0:
        yield tuple(result_list)
    else:
        for i in listunique:
            if i.occurrences > 0:
                result_list[d]=i.value
                i.occurrences-=1
                for g in  perm_unique_helper(listunique,result_list,d-1):
                    yield g
                i.occurrences+=1


def is_sorted(l):
    return all(l[i] <= l[i+1] for i in range(len(l)-1))

# def is_sorted_permutation(p):
#     # if the indeices of the first 1, 2, 3, ... is sorted
#     return is_sorted([p.index(i+1) for i in range(other_orb_color_count)])

def is_unique_permutation(p, orb_counts, first_color):
    # colors with same amount are in order
    # ex: [3, 1, 1, 2, 2] is unique (color sorted)
    # ex: [3, 2, 2, 1, 1] is not unique (equivalent to [3, 1, 1, 2, 2])

    # orb_counts[l:r] should have same values
    l = 0
    r = 1
    while l < len(orb_counts):
        while r < len(orb_counts) and orb_counts[r] == orb_counts[l]:
            r += 1
        if r - l > 1 and not is_sorted([p.index(first_color+i) for i in range(l, r)]):
            return False
        l = r
        r += 1
    return True

def unique_permutations(orb_counts, first_color):
    orbs = [color for color, count in enumerate(orb_counts, start=first_color) for i in range(count)]
    unique_permutations = [p for p in perm_unique(orbs) if is_unique_permutation(p, orb_counts, first_color)]
    return unique_permutations
