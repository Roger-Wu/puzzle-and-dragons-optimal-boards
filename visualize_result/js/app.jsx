import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";
import { BoardCard, BoardCardsContainer } from "./BoardCardsContainer.jsx";
import Select from "react-select";


function orb_config_to_url(orb_config) {
  if (!orb_config || orb_config === "optimal_boards") {
    return "https://roger-wu.github.io/puzzle-and-dragons-optimal-boards/find_optimal_boards/output/optimal_boards.json";
  }
  return "https://roger-wu.github.io/puzzle-and-dragons-optimal-boards/find_optimal_boards/output/done_" + orb_config + "/report.json";
}

class App extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.default_option_value = "optimal_boards";
    this.default_option_label = "All Optimal Boards";
    this.sorting_orders = [
      // { property: "combo_count", ascending: false},
      { property: "main_combo_count", ascending: false},
      { property: "main_matched_count", ascending: false},
      { property: "drop_times", ascending: true},
    ];

    this.state = {
      options: [{ value: this.default_option_value, label: this.default_option_label }],
      selected_option_value: this.default_option_value,
      fetched_board_data: {},
    };

    this.fetch_data = this.fetch_data.bind(this);
    this.fetch_data(this.default_option_value);
  }

  fetch_data(option_value) {
    if (!option_value) {
      option_value = this.default_option_value;
    }

    this.setState({
      selected_option_value: option_value
    });

    if (this.state.fetched_board_data.hasOwnProperty(option_value)) {
      return;
    }

    let url = orb_config_to_url(option_value);
    $.getJSON(url, (data) => {
      // console.log(data);

      if (option_value === this.default_option_value) {
        this.state.fetched_board_data[option_value] = data;
        let options = data.map((optimal_board_obj) => {
          return {
            value: optimal_board_obj.orb_config,
            label: optimal_board_obj.orb_config.replace(/-/g, " "),
          }
        });
        // prepend default option
        options.unshift({ value: this.default_option_value, label: this.default_option_label });
        this.setState({
          options: options,
          selected_option_value: option_value
        });
      }
      else {
        this.sort_boards( data.combo_to_boards[data.max_combo] );
        this.state.fetched_board_data[option_value] = data;
        this.setState({
          selected_option_value: option_value
        });
      }
    }); // .bind(this)
  }

  sort_boards(board_objs) {
    board_objs.sort((o1, o2) => {
      for (let order of this.sorting_orders) {
        let { property, ascending } = order;
        if (o1[order.property] != o2[property]) {
          return ((o1[property] < o2[property]) ^ ascending) ? 1 : -1;
        }
      }
      return 0;
    })
  }

  render() {
    return (
      <div className="app">
        <div className="top-container">
          <div className="title">
            <span className="title-text">Puzzle & Dragons Optimal Boards</span>
          </div>
          <div className="selector-wrapper">
            <Select
              value={this.state.selected_option_value}
              options={this.state.options}
              onChange={this.fetch_data}
            />
          </div>
        </div>
        {
          (!this.state.fetched_board_data.hasOwnProperty(this.state.selected_option_value)) ? (
            <Spinner />
          ) : (
            this.state.selected_option_value === this.default_option_value ? (
              <OptimalBoards board_data={this.state.fetched_board_data[this.state.selected_option_value]} />
            ) : (
              <AppBody board_data={this.state.fetched_board_data[this.state.selected_option_value]} />
            )
          )
        }
      </div>
    );
  }
}

class Spinner extends React.Component {
  render() {
    return (
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
    );
  }
}

class OptimalBoards extends React.Component {
  render() {
    console.log(this.props);
    let { board_data } = this.props;
    return (
      <div className="app-body">
        <div className="board-cards-container">
          { board_data.map((optimal_board_data) => {
            return <BoardCard
              board_obj={optimal_board_data.optimal_board_obj}
              title={optimal_board_data.orb_combination.join(" ")}
              key={optimal_board_data.orb_config}
            />
          })}
        </div>
      </div>
    )
  }
}

class AppBody extends React.Component {
  render() {
    let { board_data } = this.props;
    return (
      <div className="app-body">
        <div className="main-info-container">
          <div>
            <span className="main-info-number emphasis">{board_data.max_combo}</span>
            <span className="main-info-text"> Combos</span>
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