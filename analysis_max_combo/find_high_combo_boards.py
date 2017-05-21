from multiprocessing import Pool
from itertools import combinations, permutations, tee
import sys
import os
import time
import json
from Board import Board
# import operator as op
# from scipy.misc import comb, factorial
# from sympy.utilities.iterables import multiset_permutations


threads = 6
orb_counts = [21, 3, 3, 3]
combo_threshold = 7

orb_config_name = '-'.join(map(str, orb_counts))
output_folder = 'output/{}/'.format(orb_config_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
other_orb_colors = [i for i in range(1, len(orb_counts)) for j in range(orb_counts[i])]
other_orb_color_count = len(orb_counts) - 1

print('run with {} threads, orb counts: {}, combos >= {}'.format(threads, orb_counts, combo_threshold))
print(orb_config_name, other_orb_colors, other_orb_color_count)

# filename = 'logs/orb-18-6-6_combo-{}_fixed-{}.txt'.format(combo_threshold, fixed_pos[0])
# print('fixed_pos: {}, other_orb_colors: {}, combo_threshold: {}'.format(fixed_pos, other_orb_colors, combo_threshold))

row_size = 5
col_size = 6
orb_count = row_size * col_size
other_orb_count = len(other_orb_colors)
main_orb_count = orb_count - other_orb_count
other_orb_color_count = len(set(other_orb_colors))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

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

def is_sorted_permutation(p):
    # if the indeices of the first 1, 2, 3, ... is sorted
    return is_sorted([p.index(i+1) for i in range(other_orb_color_count)])

color_perms = list(perm_unique(other_orb_colors))
sorted_color_perms = [p for p in color_perms if is_sorted_permutation(p)]
total_perms = len(sorted_color_perms)

print('total_permutations:', total_perms)

def find_high_combo_boards_fix_first_row(fixed_first_row):
    # fixed_in_first_row = (0,)

    b = Board()

    filename = output_folder + 'fixed-{}.json'.format('-'.join(map(str, fixed_first_row)))
    out_file = open(filename, 'w')
    out_file.write('{\nboards: [\n')

    fixed_orb_count = len(fixed_first_row)
    not_fixed_orb_count = len(other_orb_colors) - len(fixed_first_row)
    total_combs = comb(24, not_fixed_orb_count)

    print('total_combinations:', total_combs)

    other_orb_max_psbl_combos = len(other_orb_colors) // 3

    found_board_count = 0
    found_combos_board_count = {}
    comb_counter = 0

    print_interval = 1000000 // len(sorted_color_perms)

    start = time.time()
    for pos_tail in combinations(range(6, 30), not_fixed_orb_count):
        # other_orb_positions
        pos = fixed_first_row + pos_tail

        main_orb_max_combos = b.count_main_orb_max_combos(pos)
        if main_orb_max_combos + other_orb_max_psbl_combos < combo_threshold:
            continue

        for colors in sorted_color_perms:
            other_orb_max_combos = b.count_other_orb_max_combos(pos, colors, other_orb_color_count)
            max_combos = main_orb_max_combos + other_orb_max_combos
            if max_combos < combo_threshold:
                continue

            b.set_sparse_board(pos, colors)
            combos, main_combos = b.count_combos()
            if combos >= combo_threshold:
                found_board_count += 1
                found_combos_board_count[combos] = found_combos_board_count.get(combos, 0) + 1
                out_file.write('{{id: {}, combos: {}, main_combos: {}, board: {}}},\n'.format(
                    found_board_count, combos, main_combos, b.get_board_string()))

        comb_counter += 1
        if comb_counter % print_interval == 0:
            proportion = comb_counter / total_combs
            elapsed_time = time.time() - start
            remaining_time = elapsed_time / proportion * (1 - proportion)
            print('fixed: {}, {:.4f} %, comb: {}, found: {}, elapsed: {:.2f}, remaining: {:.2f}'.format(
                fixed_first_row,
                proportion * 100,
                comb_counter,
                found_board_count,
                elapsed_time,
                remaining_time)
            )

    out_file.write('],\ncombos: ' + str(found_combos_board_count) + '\n}\n')
    out_file.close()

    return (list(fixed_first_row), found_combos_board_count)

def reverse_first_row(positions):
    return tuple(5 - p for p in reversed(positions))

def main():

    pool = Pool(threads)

    fixed_first_row_positions = []
    for i in range(6):
        fixed_count = i + 1
        for combi in combinations(range(6), fixed_count):
            if reverse_first_row(combi) not in fixed_first_row_positions:
                fixed_first_row_positions.append(combi)
    print(fixed_first_row_positions)


    start = time.time()

    results = pool.map(find_high_combo_boards_fix_first_row, fixed_first_row_positions)

    elapsed_time = time.time() - start
    print('total time:', elapsed_time)


    total = {}
    for fixed, found_combos_board_count in results:
        print(found_combos_board_count)
        for combos in found_combos_board_count.keys():
        	total[combos] = total.get(combos, 0) + found_combos_board_count[combos]
    print(total)


    filename = output_folder + 'log.json'
    out_file = open(filename, 'w')
    out_file.write('{\n')
    out_file.write('orb_config: ' + str(orb_config_name) + ',\n')
    out_file.write('combo_threshold: ' + str(combo_threshold) + ',\n')
    out_file.write('fixed_orbs_and_result: [\n' + ',\n'.join(map(str, results)) + '\n],\n')
    out_file.write('combos_to_boards: ' + str(total) + ',\n')
    out_file.write('threads: ' + str(threads) + ',\n')
    out_file.write('cost_time: ' + str(elapsed_time) + '\n')
    out_file.write('}\n')
    out_file.close()

def test():
    positions = range(12)
    print(positions, other_orb_colors)
    print(calc_other_orb_max_combos(positions, other_orb_colors))
    print(calc_other_orb_max_combos([0, 1, 2, 3, 4, 5, 8, 11, 17], [1, 1, 1, 2, 2, 1, 2, 1, 1]))
    # print(calc_main_orb_max_combos(positions))
    # print(predict_combos_same_color_orbs(positions))

if __name__ == '__main__':
    main()
    # test()