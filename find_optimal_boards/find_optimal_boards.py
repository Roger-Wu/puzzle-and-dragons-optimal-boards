from multiprocessing import Pool
from itertools import combinations, permutations, tee
from collections import defaultdict
import sys
import os
import time
import json
from board import Board
from utils import comb, unique_permutations


# configs
threads = 4
orb_counts = [20, 3, 3, 3, 1]
combo_threshold = 8

# constants
row_size = 5
col_size = 6
orb_count = row_size * col_size
main_color = 6
first_other_color = 1

if sum(orb_counts) != orb_count:
    print('error: number of orbs not {}'.format(orb_count))
    sys.exit()

orb_counts.sort(reverse=True)
print('execute with {} threads, orb counts: {}, combos >= {}'.format(threads, orb_counts, combo_threshold))

orb_combination_name = '-'.join(map(str, orb_counts))
output_folder = 'output/{}/'.format(orb_combination_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

main_orb_count = orb_counts[0]
other_orb_counts = orb_counts[1:]
other_orb_count = sum(other_orb_counts)
other_orb_color_count = len(other_orb_counts)
# other_orb_colors = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
# other_orb_colors = [color for i in range(1, len(orb_counts)) for repeat in range(orb_counts[i])]

other_orb_unique_color_perms = unique_permutations(other_orb_counts, first_other_color)
print('total_permutations:', len(other_orb_unique_color_perms))

def find_high_combo_boards_fix_first_row(fixed_first_row):
    # input: fixed_in_first_row = (0,)

    b = Board()
    main_color = b.main_color

    may_be_symmetric = (fixed_first_row == b.calc_symmetric_positions(fixed_first_row))
    if may_be_symmetric:
        calced_pos_ints = set()

    fixed_orb_count = len(fixed_first_row)
    not_fixed_orb_count = other_orb_count - len(fixed_first_row)
    total_combs = comb(24, not_fixed_orb_count)
    print('total_combinations:', total_combs)

    other_orb_max_psbl_combos = other_orb_count // 3

    found_board_count = 0
    combo_to_board_count = defaultdict(int)
    comb_counter = 0

    print_interval = 1000000 // len(other_orb_unique_color_perms)

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

        for colors in other_orb_unique_color_perms:
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
    for fixed_count in range(min(6, other_orb_count) + 1):
        for combi in combinations(range(col_size), fixed_count):
            if reverse_first_row(combi) not in fixed_first_row_positions:
                fixed_first_row_positions.append(combi)
    # print(fixed_first_row_positions)
    print('total processes:', len(fixed_first_row_positions))
    print('\n==== start processing ====')

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

def test():
    color_perms = unique_permutations([3, 3, 2, 2], 1)
    print(color_perms)
    print(len(color_perms))

    # positions = range(12)
    # print(positions, other_orb_colors)
    # print(calc_other_orb_max_combos(positions, other_orb_colors))
    # print(calc_other_orb_max_combos([0, 1, 2, 3, 4, 5, 8, 11, 17], [1, 1, 1, 2, 2, 1, 2, 1, 1]))
    # print(calc_main_orb_max_combos(positions))
    # print(predict_combos_same_color_orbs(positions))

if __name__ == '__main__':
    main()
    # test()