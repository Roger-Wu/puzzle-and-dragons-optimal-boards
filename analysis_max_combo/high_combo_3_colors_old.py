"""
WLOG, first orb must be in the top row and in the first 3 column
and no orb left to it

total combinations:
P(29, 11) / 2! / 3! / 3! / 3! +
P(28, 11) / 2! / 3! / 3! / 3! +
P(27, 11) / 2! / 3! / 3! / 3!
= 6.38 * 10^12

0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
1 0 0 0 0 0
"""

from itertools import combinations, permutations
import sys
# import operator as op
from scipy.misc import comb, factorial
# from sympy.utilities.iterables import multiset_permutations
import time
from Board import Board

# def ncr(n, r):
#     r = min(r, n-r)
#     if r == 0: return 1
#     numer = reduce(op.mul, xrange(n, n-r, -1))
#     denom = reduce(op.mul, xrange(1, r+1))
#     return numer//denom

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

def is_sorted_permutation(p):
    # if the indeices of the first 1, 2, 3, 4 is sorted
    return is_sorted([p.index(i+1) for i in range(4)])

def predict_combos_same_color_orbs(positions):
    rows = set()
    cols = set()
    for p in positions:
        row = p // 6
        col = p % 6
        rows.add(row)
        cols.add(col)

    row_max_combos = 0
    if len(rows) == 5:
        row_max_combos = 6
    else:
        row_max_combos = len(rows) - 1

    col_max_combos = (6 - len(cols)) + (18 - 5 * (6 - len(cols))) // 3

    return min(row_max_combos, col_max_combos)


def calc_max_combos(cols):
    cols = sorted(cols)
    used = [False] * len(cols)
    combos = 0
    for i1 in range(len(cols)):
        if used[i1]:
            continue
        for i2 in range(i1+1, len(cols)):
            if used[i2]:
                continue
            for i3 in range(i2+1, len(cols)):
                if used[i3]:
                    continue
                if cols[i1] == cols[i2] == cols[i3] or cols[i1] == cols[i2]-1 == cols[i3]-2:
                    used[i1] = True
                    used[i2] = True
                    used[i3] = True
                    combos += 1
    return combos

def predict_combos_diff_color_orbs(positions, colors):
    color_cols = [[], [], [], []]
    for p, c in zip(positions, colors):
        col = p % 6
        color_cols[c-1].append(col)

    combos = 0
    # different color orbs
    for cols in color_cols:
        combos += calc_max_combos(cols)

    return combos

def main():
    different_color_orbs = [1] * 6 + [2] * 6  # [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
    color_perms = list(perm_unique(different_color_orbs))
    sorted_color_perms = color_perms
    total_color_perms = len(sorted_color_perms)

    combo_threshold = 8
    comb_counter = 0
    found = 0
    b = Board()

    fixed_pos = (0, 1)
    f = open('logs/orb-18-6-6_combo-8_fixed-0.txt', 'w')
    f.write('[\n')

    fixed_count = len(fixed_pos)
    fixed_max = max(fixed_pos)
    total_combs = int(comb(30 - fixed_count, 12 - fixed_count))

    print('total_combinations:', total_combs)
    print('total_permutations:', total_color_perms)
    print('total:', total_combs * total_color_perms)


    start = time.time()
    for partial_c in combinations(range(fixed_max+1, 30), 12-fixed_count):
        c = fixed_pos + partial_c

        same_color_combos = predict_combos_same_color_orbs(c)
        if same_color_combos + 4 >= combo_threshold:
            for p in sorted_color_perms:
                diff_color_combos = predict_combos_diff_color_orbs(c, p)
                max_combos = same_color_combos + diff_color_combos
                if max_combos < combo_threshold:
                    continue

                b.set_sparse_board(c, p)
                combos, main_combos = b.count_combos()
                if combos >= combo_threshold:
                    found += 1
                    f.write('{{id: {}, combos: {}, main_combos: {}, board: {}}},\n'.format(found, combos, main_combos, b.get_board_string()))


        comb_counter += 1
        if comb_counter % 10 == 0:
            proportion = comb_counter / total_combs
            elapsed_time = time.time() - start
            remaining_time = elapsed_time / proportion * (1 - proportion)
            print('{:.5f} %, comb: {}, elapsed: {:.2f}, remaining: {:.2f}'.format(
                proportion * 100,
                comb_counter,
                elapsed_time,
                remaining_time),
                end='\r')

    f.write(']\n')

    # print(comb_counter)

    # print(list(permutations([1, 1, 2])))

    # print(list(perm_unique([1, 1, 2])))  # faster
    # print(list(multiset_permutations([1, 1, 2])))



if __name__ == '__main__':
    main()