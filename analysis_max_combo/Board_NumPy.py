"""
coordinates:
[
    [00, 01, 02, 03, 04, 05],  # bottom
    [10, 11, 12, 13, 14, 15],
    [20, 21, 22, 23, 24, 25],
    [30, 31, 32, 33, 34, 35],
    [40, 41, 42, 43, 44, 45],  # top
]
"""

from copy import deepcopy
import random
import numpy as np
import time


class Board(object):
    def __init__(self, board=None):
        self.height = 5
        self.width = 6
        self.row_size = 5
        self.col_size = 6
        self.orb_types = 6
        self.match_len = 3
        if board:
            self.board = np.asarray(board)
        else:
            self.set_empty_board()

    def set_empty_board(self):
        self.board = np.zeros((self.row_size, self.col_size))

    def set_random_board(self):
        self.board = [[random.randrange(1, self.orb_types + 1) \
        for j in range(self.width)] for i in range(self.height)]

    def set_sparse_board(self, positions, colors):
        # for ri in range(self.height):
        #     for ci in range(self.width):
        #         self.board[ri][ci] = self.orb_types
        self.board = [[self.orb_types for j in range(self.width)] for i in range(self.height)]
        for i in range(len(positions)):
            self.board[i // self.col_size][i % self.col_size] = colors[i]

    def get_board_string(self):
        s = ''
        for ri in range(self.row_size -1, -1, -1):
            s += ' '.join(list(map(str, self.board[ri])))
            s += '\n'
        return s

    def print_board(self):
        for row in self.board[::-1]:
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
            # board = deepcopy(self.board)
            board = self.board

        # set matched to 1 if orb matched
        matched = [[0 for j in range(self.width)] for i in range(self.height)]
        # check horizontal
        for ri in range(self.height):
            for ci in range(self.width - self.match_len + 1):
                if board[ri][ci] <= 0:
                    continue
                if board[ri][ci] == board[ri][ci+1] == board[ri][ci+2]:
                    matched[ri][ci] = 1
                    matched[ri][ci+1] = 1
                    matched[ri][ci+2] = 1
        # check vertical
        for ri in range(self.height - self.match_len + 1):
            for ci in range(self.width):
                if board[ri][ci] <= 0:
                    continue
                if board[ri][ci] == board[ri+1][ci] == board[ri+2][ci]:
                    matched[ri][ci] = 1
                    matched[ri+1][ci] = 1
                    matched[ri+2][ci] = 1

        # connect matched orbs and count combos
        combo_idxs = [[0 for j in range(self.width)] for i in range(self.height)]
        next_combo_idx = 1
        for ri in range(self.height):
            for ci in range(self.width):
                if not matched[ri][ci]:
                    continue
                if combo_idxs[ri][ci] != 0:
                    continue
                # # find all matched and connected orbs with dfs
                # stack = [(ri, ci)]
                # while stack:
                #     rj, cj = stack.pop()
                #     combo_idxs[rj][cj] = next_combo_idx
                #     if cj+1 < self.width and board[rj][cj+1] == board[rj][cj] and matched[rj][cj+1] == 1:
                #         stack.append((rj, cj+1))
                #     if rj+1 < self.height and board[rj+1][cj] == board[rj][cj] and matched[rj+1][cj] == 1:
                #         stack.append((rj+1, cj))
                # next_combo_idx += 1

                # find all matched and connected orbs with dfs
                queue = [(ri, ci)]
                ptr = 0
                while ptr < len(queue):
                    rj, cj = queue[ptr]
                    combo_idxs[rj][cj] = next_combo_idx
                    if cj+1 < self.width and board[rj][cj+1] == board[rj][cj] and matched[rj][cj+1] == 1:
                        queue.append((rj, cj+1))
                    if rj+1 < self.height and board[rj+1][cj] == board[rj][cj] and matched[rj+1][cj] == 1:
                        queue.append((rj+1, cj))
                    ptr += 1
                next_combo_idx += 1

        # self.print_board(matched)
        # self.print_board(combo_idxs)

        combo_count = next_combo_idx - 1

        if combo_count > 0:
            # remove matched orbs
            board_after = [[0 for j in range(self.width)] for i in range(self.height)]
            for ci in range(self.col_size):
                ri_after = 0
                for ri in range(self.row_size):
                    if not matched[ri][ci]:
                        board_after[ri_after][ci] = board[ri][ci]
                        ri_after += 1

            # self.print_board(board_after)

            combo_count += self.count_combos(board_after)

        return combo_count


def main():
    b = Board([
        [1, 1, 1, 2, 2, 2],
        [1, 1, 1, 2, 2, 2],
        [3, 3, 3, 2, 2, 2],
        [1, 1, 3, 3, 3, 2],
        [3, 4, 1, 1, 2, 2],
    ])
    b.print_board()

    start = time.time()
    for i in range(100):
        b.count_combos()
    print('elapsed: {}'.format(time.time() - start))

if __name__ == '__main__':
    main()