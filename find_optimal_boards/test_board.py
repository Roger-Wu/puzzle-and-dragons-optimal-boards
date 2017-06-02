import unittest
import time
from board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_other_orb_max_combos(self):
        self.assertEqual(
            self.board.calc_other_orb_max_combos(
                [0, 1, 2, 27, 28, 29],
                [1, 1, 1, 2, 2, 2]
            ), 2)

    def test_calc_max_combo_from_col_distr(self):
        self.assertEqual(self.board.calc_max_combo_from_col_distr((1, 1, 1, 0, 0, 0)), 1)
        self.assertEqual(self.board.calc_max_combo_from_col_distr((0, 0, 0, 1, 1, 1)), 1)
        self.assertEqual(self.board.calc_max_combo_from_col_distr((3, 0, 0, 0, 0, 0)), 1)
        self.assertEqual(self.board.calc_max_combo_from_col_distr((0, 0, 0, 0, 0, 3)), 1)
        self.assertEqual(self.board.calc_max_combo_from_col_distr((4, 1, 1, 0, 0, 0)), 2)
        self.assertEqual(self.board.calc_max_combo_from_col_distr((0, 0, 0, 1, 1, 4)), 2)
        self.assertEqual(self.board.calc_max_combo_from_col_distr((1, 3, 1, 1, 1, 0)), 2)

def test():
    b = Board([
        [6, 6, 3, 6, 6, 6],
        [6, 6, 2, 6, 6, 6],
        [6, 6, 1, 6, 6, 6],
        [4, 4, 4, 2, 2, 6],
        [1, 1, 2, 3, 3, 3],
    ])

    start = time.time()

    # b.print_board()
    # out = b.get_output_board()
    # print(out)
    # b.set_board_with_output_board(out)
    # b.print_board()


    # pos = (1, 6, 8, 13)
    # print(b.calc_symmetric_positions(pos))
    # print(bin(b.positions_to_int(pos)))

    # print(b.count_combos(skydrop=True))
    # for i in range(10):
    #     print(b.count_combos(skydrop=True))

    for i in range(10):
        b.calc_max_combo_from_col_distr((1, 1, 1, 0, 0, 0))
        b.calc_max_combo_from_col_distr((0, 0, 0, 1, 1, 1))
        b.calc_max_combo_from_col_distr((3, 0, 0, 0, 0, 0))
        b.calc_max_combo_from_col_distr((0, 0, 0, 0, 0, 3))
        b.calc_max_combo_from_col_distr((3, 0, 0, 0, 0, 3))
        b.calc_max_combo_from_col_distr((1, 3, 1, 1, 1, 0))


    # for i in range(10):
    #     print(b.calc_average_main_damage(10000))

    # # test count combos
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

    unittest.main()

if __name__ == '__main__':
    test()
