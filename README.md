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

[See all the visualized results here](https://roger-wu.github.io/puzzle-and-dragons-optimal-boards/visualize_result/optimal_boards.html)
