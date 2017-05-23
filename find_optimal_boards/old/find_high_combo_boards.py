from multiprocessing import Pool
from itertools import combinations, permutations, tee
from collections import defaultdict
import sys
import os
import time
import json
from Board import Board
from visualize_boards import report_to_html
# import operator as op
# from scipy.misc import comb, factorial
# from sympy.utilities.iterables import multiset_permutations


threads = 4
orb_counts = [20, 10]
combo_threshold = 7

orb_combination_name = '-'.join(map(str, orb_counts))
output_folder = 'output/{}/'.format(orb_combination_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
other_orb_colors = [i for i in range(1, len(orb_counts)) for j in range(orb_counts[i])]
other_orb_color_count = len(orb_counts) - 1

print('run with {} threads, orb counts: {}, combos >= {}'.format(threads, orb_counts, combo_threshold))
print(orb_combination_name, other_orb_colors, other_orb_color_count)

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

def positions_to_int(positions):
    pass

color_perms = list(perm_unique(other_orb_colors))
sorted_color_perms = [p for p in color_perms if is_sorted_permutation(p)]
total_perms = len(sorted_color_perms)

print('total_permutations:', total_perms)

def find_high_combo_boards_fix_first_row(fixed_first_row):
    # input: fixed_in_first_row = (0,)

    b = Board()
    main_color = b.main_color

    may_be_symmetric = (fixed_first_row == b.calc_symmetric_positions(fixed_first_row))
    if may_be_symmetric:
        calced_pos_ints = set()

    fixed_orb_count = len(fixed_first_row)
    not_fixed_orb_count = len(other_orb_colors) - len(fixed_first_row)
    total_combs = comb(24, not_fixed_orb_count)
    print('total_combinations:', total_combs)

    other_orb_max_psbl_combos = len(other_orb_colors) // 3

    found_board_count = 0
    combo_to_board_count = defaultdict(int)
    comb_counter = 0

    print_interval = 1000000 // len(sorted_color_perms)

    boards = []

    start = time.time()
    for pos_tail in combinations(range(6, 30), not_fixed_orb_count):
        # other_orb_positions
        pos = fixed_first_row + pos_tail
        if may_be_symmetric:
            pos_int = b.positions_to_int(pos)
            sym_pos_int = b.calc_symmetric_positions_int(pos)
            if sym_pos_int in calced_pos_ints:
                continue
            else:
                calced_pos_ints.add(pos_int)

        main_orb_max_combos = b.count_main_orb_max_combos(pos)
        if main_orb_max_combos + other_orb_max_psbl_combos < combo_threshold:
            continue

        for colors in sorted_color_perms:
            other_orb_max_combos = b.count_other_orb_max_combos(pos, colors, other_orb_color_count)
            max_combos = main_orb_max_combos + other_orb_max_combos
            if max_combos < combo_threshold:
                continue

            b.set_sparse_board(pos, colors)
            combos, drop_times = b.count_combos()

            combo_count = len(combos)
            main_combo_count = sum(color == main_color for color, matched in combos)
            main_matched_count = sum(matched for color, matched in combos if color == main_color)

            if combo_count >= combo_threshold:
                found_board_count += 1
                combo_to_board_count[combo_count] += 1
                boards.append({
                    'combo_count': combo_count,
                    'main_combo_count': main_combo_count,
                    'main_matched_count': main_matched_count,
                    'drop_times': drop_times,
                    'combos': combos,
                    'board': b.get_output_board()
                })

        comb_counter += 1
        if comb_counter % print_interval == 0:
            proportion = comb_counter / total_combs
            elapsed_time = time.time() - start
            remaining_time = elapsed_time / proportion * (1 - proportion)
            print('fixed: {}, {:.2f} %, comb: {}, found: {}, elapsed: {:.1f}, remaining: {:.1f}'.format(
                fixed_first_row,
                proportion * 100,
                comb_counter,
                found_board_count,
                elapsed_time,
                remaining_time)
            )

    data = {'combo_to_board_count': combo_to_board_count, 'boards': boards}
    filename = output_folder + 'fixed-{}.json'.format('-'.join(map(str, fixed_first_row)))
    with open(filename, 'w') as out_file:
        json.dump(data, out_file, indent=4)

    return data

def reverse_first_row(positions):
    return tuple(5 - p for p in reversed(positions))

def main():
    pool = Pool(threads)

    fixed_first_row_positions = []
    for fixed_count in range(7):
        for combi in combinations(range(6), fixed_count):
            if reverse_first_row(combi) not in fixed_first_row_positions:
                fixed_first_row_positions.append(combi)
    print(fixed_first_row_positions)
    print(len(fixed_first_row_positions))

    # find high combo boards
    start = time.time()
    data_list = pool.map(find_high_combo_boards_fix_first_row, fixed_first_row_positions)
    elapsed_time = time.time() - start
    print('total time:', elapsed_time)


    combo_to_board_count = defaultdict(int)
    combo_to_boards = defaultdict(list)
    for data in data_list:
        local_combo_to_board_count = data['combo_to_board_count']
        local_boards = data['boards']

        for combo in local_combo_to_board_count.keys():
            combo_to_board_count[combo] += local_combo_to_board_count[combo]

        for board in local_boards:
            combo_to_boards[board['combo_count']].append(board)

    print(combo_to_board_count)

    max_combo = max(combo_to_board_count.keys())

    report_filename = 'report.json'
    with open(output_folder + report_filename, 'w') as out_file:
        data = {
            'orb_combination': orb_counts,
            'combo_threshold': combo_threshold,
            'threads': threads,
            'cost_time': elapsed_time,
            'max_combo': max_combo,
            'combo_to_board_count': combo_to_board_count,
            'combo_to_boards': combo_to_boards,
        }
        json.dump(data, out_file, indent=4)

    report_to_html(output_folder, report_filename)

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