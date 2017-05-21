# print boards with color

import json
import sys
# from termcolor import colored


folder = 'output/done_21-9/'
name = 'combos-8'
input_filename = folder + name + '.json'
# if len(sys.argv) >= 2:
#     input_filename = sys.argv[1]
output_filename = folder + 'boards_' + name + '.html'


css = """<style>
body {
    font-family: Helvetica, Arial, sans-serif;
}
.color-1 { background-color: red; }
.color-2 { background-color: blue; }
.color-3 { background-color: green; }
.color-4 { background-color: yellow; }
.color-6 { background-color: gray; }
.board-block {
    display: inline-block;
    width: 200px;
    margin: 10px;
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

header = """<!DOCTYPE html>
<html>
<head>
""" + css + """</head>
<body>
"""

footer = """</body>
</html>
"""

def html_orb(color_idx):
    return '<span class="orb color-{}"></span>'.format(color_idx)

def html_board(board):
    html = ''
    for row_str in board:
        html += '<div class="board-row">\n'
        for color_idx in map(int, row_str.split()):
            html += html_orb(color_idx)
        html += '</div>\n'
    return html

with open(input_filename) as in_file:
    data = json.load(in_file)
    html = header
    for idx, board_obj in enumerate(data['boards']):
        html += '<div class="board-block">'
        html += '<div class="board-index"># {}</div>'.format(idx+1)
        html += '<div class="board-info">{} combos, {} main combos</div>'.format(board_obj['combos'], board_obj['main_combos'])
        html += '<div class="board">' + html_board(board_obj['board']) + '</div>'
        html += '</div>\n'
    html += footer

    with open(output_filename, 'w') as out_file:
        out_file.write(html)

