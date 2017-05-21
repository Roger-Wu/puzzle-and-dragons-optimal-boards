# print boards with color

import json
import sys
# from termcolor import colored


folder = 'output/done_24-6/'
report_filename = 'report.json'
# if len(sys.argv) >= 2:
#     input_filename = sys.argv[1]

css = """<style>
body {
    font-family: Helvetica, Arial, sans-serif;
}
.main-info {
    font-size: 24px;
}
.color-1 { background-color: red; }
.color-2 { background-color: blue; }
.color-3 { background-color: green; }
.color-4 { background-color: yellow; }
.color-6 { background-color: gray; }
.board-block {
    display: inline-block;
    width: 180px;
    margin: 15px;
}
.board-index {
    font-size: 18px;
}
.board-info {
    font-size: 14px;
    color: #404040;
    margin-bottom: 4px;
}
.board {
}
.board-row {
    height: 30px;
}
.orb {
    display: inline-block;
    width: 28px;
    height: 28px;
    border-radius:100%;
    margin: 1px;
}
</style>
"""

html_header = """<!DOCTYPE html>
<html>
<head>
""" + css + """</head>
<body>
"""

html_footer = """</body>
</html>
"""

def wrap_html(tag, class_str, contents):
    if class_str:
        return '<{} class="{}">{}</{}>'.format(tag, class_str, ''.join(contents), tag)
    else:
        return '<{}>{}</{}>'.format(tag, ''.join(contents), tag)

def html_orb(color_idx):
    return wrap_html('span', 'orb color-' + str(color_idx), '')

def html_board(board):
    html_rows = []
    for row_str in board:
        color_idxs = map(int, row_str.split())
        html_orbs = [html_orb(color_idx) for color_idx in color_idxs]
        html_row = wrap_html('div', 'board-row', html_orbs)
        html_rows.append(html_row)
    return wrap_html('div', 'board', html_rows)

def report_to_html(folder, report_filename):
    with open(folder + report_filename) as in_file:
        data = json.load(in_file)
        max_combo = data['max_combo']
        max_combo_boards = data['combo_to_boards'][str(max_combo)]

        html = html_header
        html += wrap_html('div', 'main-info', [
            wrap_html('div', '', 'Orb Combination: {}'.format(' '.join(map(str, data['orb_combination'])))),
            wrap_html('div', '', 'Max Possible Combos: {}'.format(max_combo)),
            wrap_html('div', '', 'Boards with Max Combos: {}'.format(len(max_combo_boards))),
        ])
        for idx, board_obj in enumerate(max_combo_boards):
            html += wrap_html('div', 'board-block', [
                wrap_html('div', 'board-index', '# {}'.format(idx+1)),
                wrap_html('div', 'board-info', '{} combos,<br />{} main combos,<br />{} main orbs matched,<br />drop {} times'.format(board_obj['combo_count'], board_obj['main_combo_count'], board_obj['main_matched_count'], board_obj['drop_times'])),
                html_board(board_obj['board']),
            ])
        html += html_footer

        output_filename = 'orb-{}_combo-{}.html'.format('-'.join(map(str, data['orb_combination'])), str(data['max_combo']))
        with open(folder + output_filename, 'w') as out_file:
            out_file.write(html)

if __name__ == '__main__':
    report_to_html(folder, report_filename)
