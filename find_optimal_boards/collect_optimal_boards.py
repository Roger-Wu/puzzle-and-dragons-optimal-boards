# collect max-combo boards from report.json files

import json
import os
import re
from collections import OrderedDict
from functools import cmp_to_key
import gzip
import shutil


output_folder = 'output/compact/'
folder_prefix = 'done_'
report_file_name = 'report.json'
output_file_name = 'optimal_boards.json'

orb_config_names = []
# folder_names = os.listdir(output_folder)
# print(folder_names)  # ['done_16-14', 'done_17-13', ...]

# compare_order = [
#     ('combo_count', 1),
#     ('main_combo_count', 1),
#     ('matched_main_count', 1),
#     ('matched_count', 1),
#     ('drop_times', -1)
# ]
# def compare(obj1, obj2):
#     for property, higher_better in compare_order:
#         if obj1[property] != obj2[property]:
#             if obj1[property] > obj2[property]:
#                 return higher_better
#             else:
#                 return higher_better * -1
#     return 0

optimal_board_objs = []

for folder_name in os.listdir(output_folder):
    if not folder_name.startswith(folder_prefix):
        continue

    orb_config = folder_name[len(folder_prefix):]
    with open(output_folder + folder_name + '/' + report_file_name, 'r') as in_file:
        data = json.load(in_file, object_pairs_hook=OrderedDict)
        max_combo_board_objs = data['combo_to_boards'][ str(data['max_combo']) ]

        # # add more property
        # for board_obj in max_combo_board_objs:
        #     matched_count = sum([matched for color, matched in board_obj['combos']])
        #     board_obj['matched_count'] = matched_count
        #     board_obj['matched_other_count'] = matched_count - board_obj['main_matched_count']

        # max_combo_board_objs.sort(key=cmp_to_key(compare), reverse=True)

        # for board_obj in max_combo_board_objs:
        #     print(board_obj['main_combo_count'], board_obj['main_matched_count'], board_obj['matched_count'], board_obj['drop_times'])

        optimal_board_obj = OrderedDict([
            ('orb_config', orb_config),
            ('orb_combination', data['orb_combination']),
            ('max_combo', data['max_combo']),
            ('combo_to_board_count', data['combo_to_board_count']),
            ('optimal_board_obj', max_combo_board_objs[0]),
        ])
        optimal_board_objs.append(optimal_board_obj)

optimal_board_objs.sort(key=lambda obj: obj['orb_combination'])
# print(optimal_board_objs)

with open(output_folder + output_file_name, 'w') as out_file:
    json.dump(optimal_board_objs, out_file, separators=(',',':'))

# # github.io will compress json request, so we don't need this actually
# with open(output_folder + output_file_name, 'rb') as f_in:
#     with gzip.open(output_folder + output_file_name + '.gz', 'wb') as f_out:
#         shutil.copyfileobj(f_in, f_out)

