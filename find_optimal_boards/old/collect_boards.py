# collect max-combo boards from json files

import json
import os
import re
from collections import OrderedDict

specific_combos = 8
input_folder = 'output/done_21-9/'
output_filename = input_folder + 'combos-{}.json'.format(specific_combos)

collected_boards = []
for filename in os.listdir(input_folder):
    if not filename.startswith('fixed'):
        continue

    with open(input_folder + filename, 'r') as in_file:
        data = json.load(in_file, object_pairs_hook=OrderedDict)
        for obj in data['boards']:
            board = obj['board']
            if obj['combos'] == specific_combos:
                collected_boards.append(obj)

new_data = OrderedDict()
new_data['combos'] = specific_combos
new_data['board_count'] = len(collected_boards)
new_data['boards'] = collected_boards
with open(output_filename, 'w') as out_file:
    json.dump(new_data, out_file, indent=4)
