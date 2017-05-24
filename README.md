# puzzle-and-dragons-board-analysis
Find optimal boards when the number of a kind of orb > 15

## Features

### Find Optimal Boards
* multi-processing
* speed-up tricks
  * won't compute on a board symmetric to a checked board
  * won't compute on a board equivalent to a checked board
  * estimate the upper limit of number of combos before calculating the true number of combos, so we can prevent computing on obviously low-combo boards.
* output results in JSON format

### Visualize Result
* visualize the results with a webpage
  * use React.js + Webpack

## Results

[See the visualized results here](https://roger-wu.github.io/puzzle-and-dragons-optimal-boards/visualize_result/optimal_boards.html)

<table>
  <tr>
    <th>Orb Config</th>
    <th>Sample Board</th>
    <th>Optimal Combos</th>
    <th>Visulized Boards</th>
  </tr>
  <tr>
    <td>21, 9</td>
    <td><img width="180" alt="(21, 9) Sample Board" src="https://cloud.githubusercontent.com/assets/6902276/26284913/39bbb934-3e78-11e7-8ac8-5775b5df60d2.png"></td>
    <td>8 Combos (5 + 3)<br />3 Boards</td>
    <td><a href="https://rawgit.com/Roger-Wu/puzzle-and-dragons-optimal-boards/master/analysis_max_combo/output/done_21-9/orb-21-9_combo-8.html">8-Combo Boards</a></td>
  </tr>
  <tr>
    <td>21, 3, 3, 3</td>
    <td><img width="180" alt="(21, 3, 3, 3) Sample Board" src="https://cloud.githubusercontent.com/assets/6902276/26284899/ea9602a6-3e77-11e7-983d-2438f923c12e.png"></td>
    <td>8 Combos (5 + 3)<br />25 Boards</td>
    <td><a href="https://rawgit.com/Roger-Wu/puzzle-and-dragons-optimal-boards/master/analysis_max_combo/output/done_21-3-3-3/orb-21-3-3-3_combo-8.html">8-Combo Boards</a></td>
  </tr>
</table>
