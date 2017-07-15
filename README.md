# puzzle-and-dragons-board-analysis
Find optimal boards when the number of a kind of orb > 15

## Results

[See all the visualized results here](https://roger-wu.github.io/puzzle-and-dragons-optimal-boards/visualize_result/optimal_boards.html)

## Features

### Find Optimal Boards
* multi-processing
* speed-up tricks
  * only compute on one of the two symmetric boards
  * only compute on one of the equivalent boards
  * estimate the upper limit of number of combos before calculating the true number of combos, so we can prevent computing on obviously low-combo boards.
* output results in JSON format

### Visualize Result
* visualize the results with a webpage
  * use React.js + Webpack

## Usage

### Find Optimal Boards for One Combination of Orbs

* For example, I want to find all boards with 21+5+4 orbs with more than or equal to 8 combos. And I want to multi-process it with 4 threads.
  ```
  cd find_optimal_boards
  pypy3 find_optimal_boards.py 21 5 4 8 -t 4
  ```
  It will create a `report.json` file in `find_optimal_boards/output/21-5-4/`.

* We use 4 threads by default, so you can also go with
  ```
  pypy3 find_optimal_boards.py 21 5 4 8
  ```

* You can replace `pypy3` with `python3`, but `pypy3` is about 10x faster than `python3`.

### Find Optimal Boards for Multiple Combinations of Orbs
```
cd find_optimal_boards
./run.sh
python3 add_properties.py
python3 find_optimal_boards.py
```
