import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";
import BoardCardsContainer from "./BoardCardsContainer.jsx";
import Select from "react-select";
// import Select, {Option, OptGroup} from 'rc-select';

const orb_configs = ["26-4", "26-3-1", "25-5", "25-3-2", "24-6", "24-3-3", "23-7", "23-4-3", "22-8", "22-5-3", "22-3-3-2", "21-9", "21-3-3-3", "20-10", "19-11", "18-12", "17-13", "16-14"];
let initial_orb_config = "18-12";

function orb_config_to_url(orb_config) {
  return "https://roger-wu.github.io/puzzle-and-dragons-optimal-boards/find_optimal_boards/output/done_" + orb_config + "/report.json";
}

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
      selected_orb_config: initial_orb_config,
      fetched_board_data: {},
      board_data: null,
      sorting_orders: [
        // { property: "combo_count", ascending: false},
        { property: "main_combo_count", ascending: false},
        { property: "main_matched_count", ascending: false},
        { property: "drop_times", ascending: true},
      ],
    };
    this.load_orb_config = this.load_orb_config.bind(this);
    this.load_orb_config(this.state.selected_orb_config);
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

  load_orb_config(option_value) {
    // console.log(option_value);
    if (!option_value) {
      return;
    }

    let orb_config = option_value;

    // if data has been fetched, don't fetch again
    if (this.state.fetched_board_data.hasOwnProperty(orb_config)) {
      this.setState({
        board_data: this.state.fetched_board_data[orb_config],
        selected_orb_config: orb_config,
      });
      return;
    }

    this.setState({
      board_data: null,
      selected_orb_config: orb_config,
    });

    let url = orb_config_to_url(orb_config);
    $.getJSON(url, (data) => {
      // console.log(data);
      this.sort_boards( data.combo_to_boards[data.max_combo] );
      this.state.fetched_board_data[option_value] = data;
      this.setState({
        board_data: data,
        selected_orb_config: orb_config,
      });
    });
  }

  render() {
    return (
      <div className="app">
        <div className="top-container">
          <div className="title">PAD Optimal Boards</div>
          <div className="selector-wrapper">
            <Select
              value={this.state.selected_orb_config}
              options={this.state.orb_config_options}
              onChange={this.load_orb_config}
            />
          </div>
        </div>
        <AppBody board_data={this.state.board_data}/>
      </div>
    );
  }
}

class AppBody extends React.Component {
  render() {
    let board_data = this.props.board_data;
    return (
      (board_data === null) ?
      <div className="loader-wrapper">
        <div className="sk-cube-grid">
          <div className="sk-cube sk-cube1"></div>
          <div className="sk-cube sk-cube2"></div>
          <div className="sk-cube sk-cube3"></div>
          <div className="sk-cube sk-cube4"></div>
          <div className="sk-cube sk-cube5"></div>
          <div className="sk-cube sk-cube6"></div>
          <div className="sk-cube sk-cube7"></div>
          <div className="sk-cube sk-cube8"></div>
          <div className="sk-cube sk-cube9"></div>
        </div>
      </div>
      :
      <div className="app-body">
        <div className="main-info-container">
          <div>
            <span className="main-info-number emphasis">{board_data.max_combo}</span>
            <span className="main-info-text"> Combos Max</span>
          </div>
          <div>
            <span className="main-info-number emphasis">{board_data.combo_to_boards[board_data.max_combo].length}</span>
            <span className="main-info-text"> Boards</span>
          </div>
        </div>
        <BoardCardsContainer board_objs={board_data.combo_to_boards[board_data.max_combo]} />
      </div>
    );
  }
}

function main() {
  ReactDOM.render(<App />, document.getElementById("root"));
}

window.onload = main;