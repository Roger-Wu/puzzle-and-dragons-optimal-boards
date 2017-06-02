"""
board when input/output/print:
[
    [0, 0, 0, 6, 6, 6],  # top
    [6, 6, 6, 6, 6, 6],
    [6, 6, 1, 6, 6, 6],
    [4, 4, 4, 2, 2, 6],
    [1, 1, 2, 3, 3, 3],  # bottom
]
0 means empty

board stored in Board:
[
    [1, 1, 2, 3, 3, 3],  # bottom, row_idx = 0
    [4, 4, 4, 2, 2, 6],
    [6, 6, 1, 6, 6, 6],
    [6, 6, 6, 6, 6, 6],
    [0, 0, 0, 6, 6, 6],  # top, row_idx = 4
]
board[0] = [1, 1, 2, 3, 3, 3]

position index:
24 25 26 27 28 29  # top
18 19 20 21 22 23
12 13 14 15 16 17
 6  7  8  9 10 11
 0  1  2  3  4  5  # bottom
"""

# import numpy as np
import random
import operator
from functools import lru_cache
# from collections import OrderedDict


class Board(object):
    def __init__(self, board=None):
        self.height = 5
        self.width = 6
        self.row_size = 5
        self.col_size = 6
        self.orb_colors = 6
        self.main_color = 6
        self.match_len = 3
        self.cell_count = self.row_size * self.col_size  # 30
        if board:
            self.set_board(board)
        else:
            self.set_random_board()

        self.matched = [[0] * self.width for i in range(self.height)]
        self.combo_idxs = [[0] * self.width for i in range(self.height)]
        # self.queue = [None] * self.cell_count
        self.queue_ri = [0] * self.cell_count
        self.queue_ci = [0] * self.cell_count
        self.four_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        self.color_col_counts = [[0] * self.col_size for i in range(self.orb_colors + 1)]

    def set_board(self, board):
        self.board = [list(row) for row in reversed(board)]

    def set_random_board(self):
        self.board = [[random.randrange(1, self.orb_colors + 1) \
        for j in range(self.width)] for i in range(self.height)]

    def calc_symmetric_position(self, p):
        # row_idx = p // 6
        # col_idx = p % 6
        # symmetric_col_idx = (6 - 1) - col_idx
        # symmetric_p = row_idx * 6 + symmetric_col_idx
        #   = p - (p % self.col_size) + (self.col_size - 1 - p % self.col_size)
        #   = p - (p % self.col_size) * 2 + self.col_size - 1
        return p + self.col_size - 1 - (p % self.col_size) * 2

    def calc_symmetric_positions(self, positions):
        return tuple(sorted(map(self.calc_symmetric_position, positions)))

    def calc_symmetric_positions_int(self, positions):
        return self.positions_to_int(map(self.calc_symmetric_position, positions))

    def positions_to_int(self, positions):
        b = 0
        for p in positions:
            b ^= (1 << p)
        return b

    def set_sparse_board(self, positions, colors):
        # self.board = [[self.orb_colors for j in range(self.width)] for i in range(self.height)]
        for ri in range(self.height):
            for ci in range(self.width):
                self.board[ri][ci] = self.main_color

        for p, c in zip(positions, colors):
            self.board[p // self.col_size][p % self.col_size] = c

    def get_output_board(self):
        return [' '.join(map(str, row)) for row in reversed(self.board)]

    def set_board_with_output_board(self, board):
        self.board = [list(map(int, row.split())) for row in reversed(board)]

    def print_board(self, board=None):
        if not board:
            self.print_board(self.board)
        else:
            for row in reversed(board):
                print(row)
            print()

    def get_orb(self, row_idx, col_idx):
        if row_idx < 0 or row_idx >= self.height:
            return -1
        if col_idx < 0 or col_idx >= self.width:
            return -1
        return self.board[row_idx][col_idx]

    def count_combos(self, board=None, skydrop=False):
        if not board:
            board = self.board

        matched = self.matched
        combo_idxs = self.combo_idxs
        queue_ri = self.queue_ri
        queue_ci = self.queue_ci

        for ri in range(self.row_size):
            for ci in range(self.col_size):
                matched[ri][ci] = 0
                combo_idxs[ri][ci] = 0

        # find matched orbs and mark them
        # check horizontal
        for ri in range(self.row_size):
            for ci in range(self.col_size - self.match_len + 1):
                if board[ri][ci] <= 0:
                    continue
                if board[ri][ci] == board[ri][ci+1] == board[ri][ci+2]:
                    matched[ri][ci] = 1
                    matched[ri][ci+1] = 1
                    matched[ri][ci+2] = 1
        # check vertical
        for ri in range(self.row_size - self.match_len + 1):
            for ci in range(self.col_size):
                if board[ri][ci] <= 0:
                    continue
                if board[ri][ci] == board[ri+1][ci] == board[ri+2][ci]:
                    matched[ri][ci] = 1
                    matched[ri+1][ci] = 1
                    matched[ri+2][ci] = 1

        # connect matched orbs and count combos
        combo_idx = 1
        combos = []
        for ri in range(self.row_size):
            for ci in range(self.col_size):
                if not matched[ri][ci]:
                    continue
                if combo_idxs[ri][ci] != 0:
                    continue

                # find all matched and connected orbs with bfs
                queue_ri[0] = ri
                queue_ci[0] = ci
                combo_idxs[ri][ci] = combo_idx
                matched_orb_count = 1
                head = 0  # for queue
                tail = 1  # for queue
                while head < tail:
                    rj = queue_ri[head]
                    cj = queue_ci[head]
                    # check if neighbors are matched and have same color
                    for rj_delta, cj_delta in self.four_directions:
                        rk = rj + rj_delta
                        ck = cj + cj_delta
                        if (0 <= rk < self.row_size
                        and 0 <= ck < self.col_size
                        and matched[rk][ck] == 1
                        and board[rk][ck] == board[rj][cj]
                        and combo_idxs[rk][ck] == 0):
                            combo_idxs[rk][ck] = combo_idx
                            matched_orb_count += 1
                            queue_ri[tail] = rk
                            queue_ci[tail] = ck
                            tail += 1
                    head += 1
                combos.append((board[ri][ci], matched_orb_count))
                combo_idx += 1

        drop_times = 0

        if combos:
            drop_times = 1

            # remove matched orbs
            if skydrop:
                board_after = [[random.randrange(1, self.orb_colors + 1) \
                    for j in range(self.width)] for i in range(self.height)]
            else:
                board_after = [[0] * self.width for i in range(self.height)]
            for ci in range(self.col_size):
                ri_after = 0
                for ri in range(self.row_size):
                    if not matched[ri][ci]:
                        board_after[ri_after][ci] = board[ri][ci]
                        ri_after += 1

            extra_combos, extra_drop_times = self.count_combos(board_after, skydrop=skydrop)
            combos += extra_combos
            drop_times += extra_drop_times

        return combos, drop_times

    def count_main_orb_max_combos(self, other_orb_positions):
        row_size = self.row_size  # 5
        col_size = self.col_size  # 6
        match_len = self.match_len  # 3

        # use global variable will not speed up
        rows_only_main_orbs = [1] * row_size
        cols_only_main_orbs = [1] * col_size

        for p in other_orb_positions:
            rows_only_main_orbs[p // col_size] = 0
            cols_only_main_orbs[p % col_size] = 0

        rc = sum(rows_only_main_orbs)  # only_main_orb_row_count
        cc = sum(cols_only_main_orbs)  # only_main_orb_col_count

        main_orb_count = self.cell_count - len(other_orb_positions)

        if rc == cc == 0:
            return main_orb_count // match_len

        matched_main_orbs = rc * col_size + cc * row_size - rc * cc

        if rc > 0 and cc > 0:
            combos = 1
        elif rc > 0:  # cc == 0
            combos = rows_only_main_orbs[0]
            for i in range(1, row_size):
                if rows_only_main_orbs[i-1] == 0 and rows_only_main_orbs[i] == 1:
                    combos += 1
        else:
            combos = cols_only_main_orbs[0]
            for i in range(1, col_size):
                if cols_only_main_orbs[i-1] == 0 and cols_only_main_orbs[i] == 1:
                    combos += 1

        return combos + (main_orb_count - matched_main_orbs) // match_len

    def calc_other_orb_max_combos(self, other_orb_positions, other_orb_colors):
        # color_col_counts: for each color, how many orbs are in each column
        color_col_counts = self.color_col_counts
        has_colors = [False] * (self.orb_colors + 1)

        # reset to 0
        for col_counts in color_col_counts:
            for col_idx in range(len(col_counts)):
                col_counts[col_idx] = 0

        for pos, color in zip(other_orb_positions, other_orb_colors):
            col = pos % 6
            color_col_counts[color][col] += 1
            has_colors[color] = True

        max_combo_count = 0
        for color in range(len(has_colors)):
            if has_colors[color] == False:
                continue
            max_combo_count += self.calc_max_combo_from_col_distr(tuple(color_col_counts[color]))

        return max_combo_count

    @lru_cache(maxsize=10000)
    def calc_max_combo_from_col_distr(self, col_distr):
        # col_distr: how many orbs in each column, e.g. [0, 1, 2, 2, 1, 0]
        # return max possible combo count, e.g. 2
        if sum(col_distr) < self.match_len:
            return 0

        max_combo = 0

        # check vertical
        for col_idx in range(len(col_distr)):
            if col_distr[col_idx] >= self.match_len:
                new_col_distr = list(col_distr)
                new_col_distr[col_idx] -= self.match_len
                new_col_distr = tuple(new_col_distr)
                combo = 1 + self.calc_max_combo_from_col_distr(new_col_distr)
                max_combo = max(max_combo, combo)
                break

        # check horizontal
        for col_idx in range(len(col_distr) - self.match_len + 1):
            if (col_distr[col_idx] >= 1
            and col_distr[col_idx + 1] >= 1
            and col_distr[col_idx + 2] >= 1):
                new_col_distr = list(col_distr)
                for tmp_col_idx in range(col_idx, col_idx + self.match_len):
                    new_col_distr[tmp_col_idx] -= 1
                new_col_distr = tuple(new_col_distr)
                combo = 1 + self.calc_max_combo_from_col_distr(new_col_distr)
                max_combo = max(max_combo, combo)
                break

        return max_combo

    def calc_main_damage_from_combos(self, combos):
        combo_count = len(combos)
        combo_multiplier = 1 + (combo_count - 1) / 4

        main_combo_count = 0
        main_match_multiplier = 0
        for combo in combos:
            color, matched_orb_count = combo
            if color == self.main_color:
                main_combo_count += 1
                main_match_multiplier += 1 + (matched_orb_count - 3) / 4

        main_damage_multiplier = main_match_multiplier * combo_multiplier

        return {
            'combo_count': combo_count,
            'main_combo_count': main_combo_count,
            'main_damage_multiplier': main_damage_multiplier,
        }

    def calc_main_damage(self, skydrop=False):
        combos, drop_times = self.count_combos(skydrop=skydrop)
        return self.calc_main_damage_from_combos(combos)

    def calc_average_main_damage(self, simulation_times=10000):
        # if simulation_times > 1, calculate average damage
        combo_counts = []
        main_combo_counts = []
        main_damage_multipliers = []

        for simulation_idx in range(simulation_times):
            combos, drop_times = self.count_combos(skydrop=True)
            res = self.calc_main_damage_from_combos(combos)

            combo_counts.append(res['combo_count'])
            main_combo_counts.append(res['main_combo_count'])
            main_damage_multipliers.append(res['main_damage_multiplier'])

        # result = OrderedDict([
        #     ('simulation_times', simulation_times),
        #     ('combo_count_avg', sum(combo_counts) / len(combo_counts)),
        #     ('combo_count_min', min(combo_counts)),
        #     ('main_combo_count_avg', sum(main_combo_counts) / len(main_combo_counts)),
        #     ('main_damage_multiplier_avg', sum(main_damage_multipliers) / len(main_damage_multipliers)),
        #     # ('main_damage_multiplier_std', np.std(main_damage_multipliers)),
        # ])

        result = {
            'simulation_times': simulation_times,
            'combo_count_avg': sum(combo_counts) / len(combo_counts),
            'combo_count_min': min(combo_counts),
            'main_combo_count_avg': sum(main_combo_counts) / len(main_combo_counts),
            'main_damage_multiplier_avg': sum(main_damage_multipliers) / len(main_damage_multipliers),
            # 'main_damage_multiplier_std': np.std(main_damage_multipliers),
        }

        return result
