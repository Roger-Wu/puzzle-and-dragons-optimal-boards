# print boards with color

import json
import sys
# from termcolor import colored


input_filename = 'output/done_21-3-3-3/combos-8.json'
if len(sys.argv) >= 2:
    input_filename = sys.argv[1]
# orb_char = '●'
orb_char = '⬤'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

colors = ['', bcolors.FAIL, bcolors.OKGREEN, bcolors.OKBLUE, bcolors.WARNING, ]

def colored_orb_char(color_idx):
    if color_idx < len(colors):
        return colors[color_idx] + orb_char + bcolors.ENDC
    return orb_char

def print_board(board):
    for row_str in board:
        for color_idx in map(int, row_str.split()):
            print(colored_orb_char(color_idx), end='')
        print()
    print()

with open(input_filename) as in_file:
    data = json.load(in_file)
    for board_obj in data['boards']:
        print_board(board_obj['board'])
