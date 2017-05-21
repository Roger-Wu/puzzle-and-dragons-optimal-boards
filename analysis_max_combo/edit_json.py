"""
change
[
    "[6, 6, 1, 6, 6, 6]",
    "[6, 6, 1, 6, 6, 1]",
    "[6, 1, 6, 1, 1, 6]",
    "[1, 6, 1, 6, 6, 6]",
    "[1, 6, 6, 6, 6, 6]"
]
to
[
    '6 6 1 6 6 6',
    '6 6 1 6 6 1',
    '6 1 6 1 1 6',
    '1 6 1 6 6 6',
    '1 6 6 6 6 6'
]
"""

import json
import os
import re
from collections import OrderedDict

translation_table = dict.fromkeys(map(ord, '[,]'), None)

def to_compact_board(board):
    return [row.translate(translation_table) for row in board]

input_folder = 'output/done_21-9/'
output_folder = 'output/compact_done_21-9/'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if not filename.startswith('fixed'):
        continue

    with open(input_folder + filename, 'r') as in_file:
        data = json.load(in_file, object_pairs_hook=OrderedDict)
        for obj in data['boards']:
            obj['board'] = to_compact_board(obj['board'])
        new_data = OrderedDict()
        new_data['combos_boards'] = data['combos_boards']
        new_data['boards'] = data['boards']
        with open(output_folder + filename, 'w') as out_file:
            json.dump(new_data, out_file, indent=4)


# board = [
#     "[6, 6, 1, 6, 6, 6]",
#     "[6, 6, 1, 6, 6, 1]",
#     "[6, 1, 6, 1, 1, 6]",
#     "[1, 6, 1, 6, 6, 6]",
#     "[1, 6, 6, 6, 6, 6]"
# ]
# print(to_compact_board(board))
