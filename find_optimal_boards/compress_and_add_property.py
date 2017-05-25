# collect max-combo boards from report.json files

import json
import os
import re
from collections import OrderedDict
import gzip
import shutil

input_folder = 'output/'
folder_prefix = 'done_'
input_file_name = 'report.json'

output_folder = 'output/compact/'
output_file_name = 'report.json'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for folder_name in os.listdir(input_folder):
    if not folder_name.startswith(folder_prefix):
        continue

    output_sub_folder = output_folder + folder_name + '/'
    if os.path.exists(output_sub_folder):
        continue

    input_file_path = input_folder + folder_name + '/' + input_file_name
    print('compressing ' + input_file_path)

    with open(input_file_path, 'r') as in_file:
        data = json.load(in_file, object_pairs_hook=OrderedDict)

        for key in data['combo_to_boards']:
            board_objs = data['combo_to_boards'][key]

            for board_obj in board_objs:
                matched_count = sum([matched for color, matched in board_obj['combos']])
                board_obj['matched_count'] = matched_count
                board_obj['matched_main_count'] = board_obj['main_matched_count']
                board_obj['matched_other_count'] = matched_count - board_obj['main_matched_count']
                board_obj.pop('main_matched_count', None)

                board = board_obj['board']
                board_obj.pop('board', None)
                board_obj['board'] = board

    if not os.path.exists(output_sub_folder):
        os.makedirs(output_sub_folder)
    with open(output_sub_folder + output_file_name, 'w') as out_file:
        json.dump(data, out_file, separators=(',',':'))

    with open(output_sub_folder + output_file_name, 'rb') as f_in:
        with gzip.open(output_sub_folder + output_file_name + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
