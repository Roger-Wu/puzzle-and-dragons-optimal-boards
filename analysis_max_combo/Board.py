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

coordinates of board stored in Board:
[
    [00, 01, 02, 03, 04, 05],  # bottom
    [10, 11, 12, 13, 14, 15],
    [20, 21, 22, 23, 24, 25],
    [30, 31, 32, 33, 34, 35],
    [40, 41, 42, 43, 44, 45],  # top
]
"""

import random
import time


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

        self.color_col_counts = [[0] * self.col_size for i in range(self.orb_colors)]

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

    def get_board_string(self):
        return '[\n' + ',\n'.join(map(str, reversed(self.board))) + ']'

    def get_output_board(self):
        return [' '.join(map(str, row)) for row in reversed(self.board)]

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

    def count_combos(self, board=None):
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
            board_after = [[0] * self.width for i in range(self.height)]
            for ci in range(self.col_size):
                ri_after = 0
                for ri in range(self.row_size):
                    if not matched[ri][ci]:
                        board_after[ri_after][ci] = board[ri][ci]
                        ri_after += 1

            extra_combos, extra_drop_times = self.count_combos(board_after)
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

    def count_other_orb_max_combos(self, other_orb_positions, other_orb_colors, other_orb_color_count):
        col_size = self.col_size
        color_col_counts = self.color_col_counts

        for color in range(other_orb_color_count):
            for col in range(col_size):
                color_col_counts[color][col] = 0

        for p, c in zip(other_orb_positions, other_orb_colors):
            color = c - 1
            col = p % 6
            color_col_counts[color][col] += 1

        combos = 0
        for color in range(other_orb_color_count):
            col = 0
            while col < col_size:
                if color_col_counts[color][col] >= 3:
                    combos += 1
                    color_col_counts[color][col] -= 3
                    continue
                elif (col+2 < col_size
                and color_col_counts[color][col] > 0
                and color_col_counts[color][col+1] > 0
                and color_col_counts[color][col+2] > 0):
                    combos += 1
                    for i in range(3):
                        color_col_counts[color][col+i] -= 1
                else:
                    col += 1
        return combos


def main():
    b = Board([
        [6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6],
        [6, 6, 1, 6, 6, 6],
        [4, 4, 4, 2, 2, 6],
        [1, 1, 2, 3, 3, 3],
    ])

    start = time.time()

    pos = (1, 6, 8, 13)
    print(b.calc_symmetric_positions(pos))
    print(bin(b.positions_to_int(pos)))

    # print(b.count_combos())

    # test count combos
    # for i in range(10000):
    #     b.count_combos()

    # b.print_board()

    # positions = list(range(12))
    # colors = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]


    # print(b.count_combos())

    # print(b.count_main_orb_max_combos([0, 7, 14, 21, 28, 29]))
    # positions = [0, 1, 2, 3, 6, 12, 24]
    # for i in range(10000):
    #     b.count_other_orb_max_combos(positions, [1] * len(positions), 1)

    print('elapsed: {}'.format(time.time() - start))


if __name__ == '__main__':
    main()