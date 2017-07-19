import React from "react";
import { render } from "react-dom";


class Board extends React.Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      isHovered: false,
    };

    this.handleMouseEnter = this.handleMouseEnter.bind(this);
    this.handleMouseLeave = this.handleMouseLeave.bind(this);
  }

  handleMouseEnter() {
    this.setState({isHovered: true})
  }

  handleMouseLeave() {
    this.setState({isHovered: false})
  }

  render() {
    let { board } = this.props;

    let int_board = [];
    let board_str = "";
    for (let row_str of board) {
      let row = [];
      for (let color_str of row_str.split(" ")) {
        let color_idx = parseInt(color_str);
        row.push(color_idx);
        board_str += (color_idx - 1).toString();
      }
      int_board.push(row)
    }
    let url = "http://serizawa.web5.jp/puzzdra_theory_maker/index.html?layout=" + board_str + "&route=05,";
    let rows = this.props.board.map(function(row_str, index) {
      let color_strs = row_str.split(" ");
      let row_orbs = color_strs.map(function(color_str, index) {
        return React.createElement("span", {className: "orb orb-color-" + color_str, key: index}, null);
      });
      return React.createElement("div", {className: "board-row", key: index}, row_orbs);
    });
    return (
      <a href={url} target="_blank">
        <div className="board" onMouseEnter={this.handleMouseEnter} onMouseLeave={this.handleMouseLeave}>
          {rows}
          {
            (this.state.isHovered) ?
            <div className="board-play-button">&#9658;</div>
            : null
          }
        </div>
      </a>
    )
  }
}

export class BoardCard extends React.Component {
  render() {
    let { board_obj, title } = this.props;
    // let infos = [
    //   `${board_obj.combo_count} combos`,
    //   `${board_obj.main_combo_count} main combos`,
    //   `${board_obj.matched_main_count} matched main orbs`,
    //   `${board_obj.drop_times} times of dropping`,
    // ];

    return React.createElement("div", {className: "board-card"}, [
      React.createElement("div", {className: "board-index", key: "board-index"}, `${title}`),
      <div className="board-info" key="board-info">
        <div title="the number of combos of main orbs and other orbs">
          <span className="board-info-text">combos</span>
          <span className="board-info-number emphasis">
            <span>{board_obj.main_combo_count}</span>
            <span className="board-info-plus">+</span>
            <span>{board_obj.combo_count - board_obj.main_combo_count}</span>
          </span>
        </div>
        <div title="the number of matched main orbs and other orbs">
          <span className="board-info-text">orbs matched</span>
          <span className="board-info-number emphasis">
            <span>{board_obj.matched_main_count}</span>
            <span className="board-info-plus">+</span>
            <span>{board_obj.matched_other_count}</span>
          </span>
        </div>
        <div title={"the minimum number of combos when there are skydrop orbs (with " + board_obj.simulation_times.toString() + " simulations)"}>
          <span className="board-info-text">min. combos</span>
          <span className="board-info-number emphasis">{board_obj.combo_count_min}</span>
        </div>
        <div title={"the average number of combos when there are skydrop orbs (with " + board_obj.simulation_times.toString() + " simulations)"}>
          <span className="board-info-text">avg. combos</span>
          <span className="board-info-number emphasis">{board_obj.combo_count_avg.toFixed(1)}</span>
        </div>
        <div title={"the average damage multiplier when there are skydrop orbs (with " + board_obj.simulation_times.toString() + " simulations)"}>
          <span className="board-info-text">avg. damage</span>
          <span className="board-info-number emphasis">x {board_obj.main_damage_multiplier_avg.toFixed(1)}</span>
        </div>
        {/*<div>
          <span className="board-info-text">times of dropping</span>
          <span className="board-info-number emphasis">{board_obj.drop_times}</span>
        </div>*/}
      </div>,
      // infos.map(function(info) {
      //   return React.createElement("div", {className: "board-info"}, info);
      // }),
      React.createElement(Board, {board: board_obj.board, key: "board"}, null)
    ]);
  }
}

export class BoardCardsContainer extends React.Component {
  // constructor(props, context) {
  //   super(props, context);
  //   // this.showMore = this.showMore.bind(this);
  // }

  componentWillMount() {
    this.state = {
      show_board_count: 100,
    }
  }

  showMore() {
    this.setState({
      show_board_count: this.state.show_board_count + 100,
    });
  }

  render() {
    const { board_objs } = this.props;
    const { show_board_count } = this.state;

    const boards = [];
    const len = Math.min(show_board_count, board_objs.length);
    for (let i = 0; i < len; i++) {
        let board_obj = board_objs[i];
        let key = board_obj.board.join(" ");
        boards.push( React.createElement(BoardCard, {board_obj: board_obj, title: i+1, key: key}, null) );
    }

    return (
      <div className="board-cards-container">
        { boards }
        {
          (board_objs.length > show_board_count) ?
          <div onClick={this.showMore.bind(this)} className="show-more-text">Show More</div>
          : null
        }
      </div>
    )
  }
}

// export default BoardCardsContainer;
