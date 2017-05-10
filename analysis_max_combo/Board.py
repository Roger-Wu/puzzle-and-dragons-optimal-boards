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
            self.set_board(board)
        else:
            self.set_random_board()

        self.matched = [[0 for j in range(self.width)] for i in range(self.height)]
        self.combo_idxs = [[0 for j in range(self.width)] for i in range(self.height)]
        self.queue = [None] * (self.row_size * self.col_size)

    def set_board(self, board):
        self.board = board[::-1]

    def set_random_board(self):
        self.board = [[random.randrange(1, self.orb_types + 1) \
        for j in range(self.width)] for i in range(self.height)]

    def set_sparse_board(self, positions, colors):
        # self.board = [[self.orb_types for j in range(self.width)] for i in range(self.height)]
        for ri in range(self.height):
            for ci in range(self.width):
                self.board[ri][ci] = self.orb_types
        # for i in range(len(positions)):
        #     p = positions[i]
        #     self.board[p // self.col_size][p % self.col_size] = colors[i]
        for p, c in zip(positions, colors):
            self.board[p // self.col_size][p % self.col_size] = c

    def get_board_string(self):
        s = ''
        for ri in range(self.row_size -1, -1, -1):
            # s += ' '.join(list(map(str, self.board[ri])))
            s += str(self.board[ri])
            s += '\n'
        return s

    def print_board(self, board=None):
        if not board:
            self.print_board(self.board)
        else:
            for ri in range(self.row_size-1, -1, -1):
                print(board[ri])
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

        matched = self.matched
        combo_idxs = self.combo_idxs
        queue = self.queue

        for ri in range(self.row_size):
            for ci in range(self.col_size):
                matched[ri][ci] = 0
                combo_idxs[ri][ci] = 0

        # set matched to 1 if orb matched
        # matched = [[0 for j in range(self.width)] for i in range(self.height)]
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
        # combo_idxs = [[0 for j in range(self.width)] for i in range(self.height)]
        next_combo_idx = 1
        for ri in range(self.row_size):
            for ci in range(self.col_size):
                if not matched[ri][ci]:
                    continue
                if combo_idxs[ri][ci] != 0:
                    continue

                # find all matched and connected orbs with dfs
                # for i in range(len(queue)):
                #     queue[i] == None
                queue[0] = (ri, ci)
                combo_idxs[ri][ci] = next_combo_idx
                head = 0
                tail = 1
                while head < tail:
                    rj, cj = queue[head]
                    # combo_idxs[rj][cj] = next_combo_idx
                    for rj_delta, cj_delta in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        rk = rj + rj_delta
                        ck = cj + cj_delta

                        if 0 <= rk < self.row_size and 0 <= ck < self.col_size and matched[rk][ck] == 1 and board[rk][ck] == board[rj][cj] and combo_idxs[rk][ck] == 0:
                            combo_idxs[rk][ck] = next_combo_idx
                            queue[tail] = (rk, ck)
                            tail += 1

                    head += 1
                next_combo_idx += 1

        # print('matched:')
        # self.print_board(matched)
        # print('combo_idxs:')
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
        [6, 6, 6, 6, 6, 6],
        [6, 6, 6, 6, 6, 6],
        [6, 6, 1, 6, 6, 6],
        [4, 4, 4, 2, 2, 6],
        [1, 1, 2, 3, 3, 3],
    ])

    b.print_board()

    positions = list(range(12))
    colors = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]

    start = time.time()
    for i in range(10000):
        # b.set_sparse_board(positions, colors)
        b.count_combos()
    print('elapsed: {}'.format(time.time() - start))

    print(b.count_combos())

if __name__ == '__main__':
    main()