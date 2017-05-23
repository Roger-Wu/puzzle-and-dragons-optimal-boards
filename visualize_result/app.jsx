import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";
import BoardCardsContainer from "./BoardCardsContainer.jsx";
import Select from "react-select";


const orb_configs = ["24-6", "24-3-3", "23-7", "23-4-3", "22-8", "22-5-3", "22-3-3-2", "21-9", "21-3-3-3", "20-10", "19-11", "18-12", "17-13", "16-14"];

class App extends React.Component {
  constructor(props, context) {
    super(props, context)

    this.state = {
      // orb_configs: orb_configs,
      orb_config_options: orb_configs.map((orb_config) => {
        return {
          value: orb_config,
          label: orb_config.replace(/-/g, " ")
        };
      }),
      selected_value: "18-12",
      board_data: {
        orb_combination: [],
        max_combo: null,
      },
      board_objs: [],
      sorting_orders: [
        // { property: "combo_count", ascending: false},
        { property: "main_combo_count", ascending: false},
        { property: "main_matched_count", ascending: false},
        { property: "drop_times", ascending: true},
      ],
    };
    this.load_orb_config = this.load_orb_config.bind(this);
    this.load_orb_config({value: this.state.selected_value});
  }

  sort_boards(board_objs) {
    board_objs.sort((o1, o2) => {
      for (let order of this.state.sorting_orders) {
        let { property, ascending } = order;
        if (o1[order.property] != o2[property]) {
          return ((o1[property] < o2[property]) ^ ascending) ? 1 : -1;
        }
      }
      return 0;
    })
  }

  load_orb_config(option) {
    let orb_config = option.value;
    let url = "https://raw.githubusercontent.com/Roger-Wu/puzzle-and-dragons-optimal-boards/master/find_optimal_boards/output/done_" + orb_config + "/report.json";
    $.getJSON(url, (data) => {
      console.log(data);
      let max_combo_board_objs = data.combo_to_boards[data.max_combo]
      this.sort_boards(max_combo_board_objs);
      this.setState({
        board_data: data,
        board_objs: max_combo_board_objs,
        selected_value: orb_config,
      })
    });
  }

  render() {
    let { board_data, board_objs } = this.state;
    return (
      <div className="app">
        <div className="top-container">
          <div className="title">PAD Optimal Boards</div>
          <div className="selector-wrapper">
            <Select
              value={this.state.selected_value}
              options={this.state.orb_config_options}
              onChange={this.load_orb_config}
            />
          </div>
        </div>
        <div className="main-info-container">
          <div>
            <span className="main-info-number emphasis">{board_data.max_combo}</span>
            <span className="main-info-text"> Combos Max</span>
          </div>
          <div>
            <span className="main-info-number emphasis">{board_objs.length}</span>
            <span className="main-info-text"> Boards</span>
          </div>
        </div>
        <BoardCardsContainer board_objs={this.state.board_objs} />
      </div>
    );
  }
}


// function sort_boards() {
//     // displayed_board_objs.sort(function(obj1, obj2) {
//     //   // compare order: main_combo_count ^,
//     //   if (obj1.main_combo_count) {

//     //   }
//     //   else {
//     //     return obj1.
//     //   }
//     // });
// }

// function load_orb_config(orb_config) {
//   let url = "https://raw.githubusercontent.com/Roger-Wu/puzzle-and-dragons-optimal-boards/master/find_optimal_boards/output/done_" + orb_config + "/report.json";
//   $.getJSON(url, function(_data) {
//     console.log(_data);
//     data = _data;
//     displayed_board_objs = data.combo_to_boards[data.max_combo];

//     ReactDOM.render(
//       React.createElement(BoardCardsContainer, {board_objs: displayed_board_objs}, null),
//       document.getElementById("root")
//     );
//   });
// }

function main() {
  ReactDOM.render(<App />, document.getElementById("root"));
}

window.onload = main;