import $ from "jquery";
import React from "react";
import ReactDOM from "react-dom";
import { BoardCard, BoardCardsContainer } from "./BoardCardsContainer.jsx";
import Select from "react-select";


function orb_config_to_url(orb_config) {
  if (!orb_config || orb_config === "optimal_boards") {
    return "https://raw.githubusercontent.com/Roger-Wu/puzzle-and-dragons-optimal-boards/master/find_optimal_boards/output/compact/optimal_boards.json";
    // return "https://roger-wu.github.io/puzzle-and-dragons-optimal-boards/find_optimal_boards/output/compact/optimal_boards.json";
  }
  return "https://raw.githubusercontent.com/Roger-Wu/puzzle-and-dragons-optimal-boards/master/find_optimal_boards/output/compact/done_" + orb_config + "/report.json";
  // return "https://roger-wu.github.io/puzzle-and-dragons-optimal-boards/find_optimal_boards/output/compact/done_" + orb_config + "/report.json";
}

class App extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.default_option_value = "optimal_boards";
    this.default_option_label = "All Optimal Boards";
    this.sorting_orders = [
      // { property: "combo_count", ascending: false},
      { property: "main_combo_count", ascending: false},
      { property: "matched_main_count", ascending: false},
      { property: "matched_count", ascending: false},
      { property: "drop_times", ascending: true},
    ];

    this.state = {
      options: [{ value: this.default_option_value, label: this.default_option_label }],
      selected_option_value: this.default_option_value,
      fetched_board_data: {},
    };

    this.fetch_data = this.fetch_data.bind(this);
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

      // if the fetched data is all optimal boards
      if (option_value === this.default_option_value) {
        // separate data into groups by the number of main orbs
        let data_dict = {};
        for (let board_obj of data) {
          let main_orb_count = board_obj.orb_combination[0];
          if (!data_dict.hasOwnProperty(main_orb_count)) {
            data_dict[main_orb_count] = [];
          }
          data_dict[main_orb_count].push(board_obj);
        }

        this.state.fetched_board_data[option_value] = data_dict;
        let options = data.map((optimal_board_obj) => {
          return {
            value: optimal_board_obj.orb_config,
            label: optimal_board_obj.orb_combination.join(" "),
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
        // this.sort_boards( data.combo_to_boards[data.max_combo] );
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

  loadFbSdk() {
    window.fbAsyncInit = function() {
      FB.init({
        appId            : '1302050683224374',
        autoLogAppEvents : true,
        xfbml            : true,
        version          : 'v2.9'
      });
      FB.AppEvents.logPageView();
    };

    (function(d, s, id){
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) {return;}
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
  }

  componentDidMount() {
    this.loadFbSdk();
    this.fetch_data(this.default_option_value);
  }

  render() {
    return (
      <div className="app">
        <div className="top-container">
          <div className="title">
            <div className="title-text">Puzzle & Dragons</div>
            <div className="title-text">Optimal Boards</div>
          </div>
        </div>
        <div className="selector-wrapper">
          <Select
            value={this.state.selected_option_value}
            options={this.state.options}
            onChange={this.fetch_data}
          />
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
    let { board_data } = this.props;
    // board_data = {
    //   16: [{"orb_config":"16-12-2",...}, ...],
    //   17: [],
    //   ...
    // }

    let keys = Object.keys(board_data);
    keys.sort();
    let elements = [];
    for (let key of keys) {
      elements.push(
        <div className="main-info-container">
          <span className="main-info-number emphasis">{key}</span>
          <span className="main-info-text"> Orbs in One Color</span>
        </div>
      );
      let board_group = board_data[key];
      for (let one_board_data of board_group) {
        elements.push(
          <BoardCard
            board_obj={one_board_data.optimal_board_obj}
            title={one_board_data.orb_combination.join(" ")}
            key={one_board_data.orb_config}
          />
        );
      }
    }
    return (
      <div className="app-body">
        <div className="board-cards-container">
          { elements }
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