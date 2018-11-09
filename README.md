# puzzle-and-dragons-optimal-boards

An optimized brute-force searcher for the game, Puzzle & Dragons, to search for all high-combo layouts when there are 15+ orbs in the same color on a 5 x 6 board.

![demo image](https://raw.githubusercontent.com/Roger-Wu/puzzle-and-dragons-optimal-boards/master/visualize_result/images/demo.png)

## Results

[**See all the optimal boards here**](https://roger-wu.github.io/puzzle-and-dragons-optimal-boards/visualize_result/optimal_boards.html)

## Features

### Finding Optimal Boards
* multi-processing
* speed-up tricks
  * only compute on one of the two symmetric boards
  * only compute on one of the equivalent boards
  * estimate the upper limit of number of combos before calculating the true number of combos, so we can prevent computing on obviously low-combo boards.
* output results in JSON format

### Visualizing Boards
* visualize the results with a webpage
  * written with React.js + Webpack
* orb matching animation
  * using [@powder0326's website](http://serizawa.web5.jp/puzzdra_theory_maker/index.html)

## How to Use

### Requirements

* For finding optimal boards, you need `python3` and `pypy3`
* For visualizing the boards, you need `node.js` and `npm`.

### Step 1. Find Optimal Boards Given an Orb Combination

* For example, I want to find all boards with 21+5+4 orbs with more than or equal to 8 combos. And I want to multi-process it with 4 threads.
  ```
  $ cd find_optimal_boards
  $ pypy3 find_optimal_boards.py 21 5 4 8 -t 4
  ```
  It will output a `report.json` file in `find_optimal_boards/output/21-5-4/`.

* The program runs with 4 threads by default, so you can also go with
  ```
  $ pypy3 find_optimal_boards.py 21 5 4 8
  ```

* We recommend using `pypy3` because it's about 10x faster than `python3` in our case. But if you don't have `pypy3` installed, you can still run with `python3`. For example,
  ```
  $ python3 find_optimal_boards.py 21 5 4 8
  ```

* While the program is running, it outputs some temporary results, like `fixed-0-2.json`, in `find_optimal_boards/output/21-5-4/`. If the program stops running for some reasons, the next time you run the program, it will automatically resume from the previous breakpoint.

### Step 2. Simulate Orb Matching and Find the Best Board

* After `find_optimal_boards.py` finishes running, you get a `report.json` file in a folder named with the orb combination, like `find_optimal_boards/output/21-5-4/report.json`

* First, rename the folder to `21-5-4/` `done_21-5-4/` to let our programs know that it's a finished one.
  
* Run 
  ```
  $ pypy3 add_properties.py
  ```
  to simulate orb matching and get some statistics like average number of combos and average damage of each board.
  It will read the boards in `find_optimal_boards/output/done_21-5-4/report.json`, do the simulations, add some properties to it, and output another json file `find_optimal_boards/output/compact/done_21-5-4/report.json`.

### Step 3. Collect the Boards with Highest Damages

* After you have run Step 1 and 2 for multiple orb combinations, you get many `report.json`. It's time to get the best boards together, so the PAD players can easily find the boards with highest damages.
* Run
  ```
  $ pypy3 collect_optimal_boards.py
  ```
  and it will read all the `report.json` in `find_optimal_boards/output/compact/done_xxx/` and extract the boards with highest damages and output them to `find_optimal_boards/output/compact/optimal_boards.json`
  
