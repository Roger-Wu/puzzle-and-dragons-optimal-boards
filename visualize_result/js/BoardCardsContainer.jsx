import React from "react";
import { render } from "react-dom";


class Board extends React.Component {
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
        {React.createElement("div", {className: "board"}, rows)}
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
        <div>
          <span className="board-info-text">combos</span>
          <span className="board-info-number emphasis">
            <span>{board_obj.main_combo_count}</span>
            <span className="board-info-plus">+</span>
            <span>{board_obj.combo_count - board_obj.main_combo_count}</span>
          </span>
        </div>
        <div>
          <span className="board-info-text">orbs matched</span>
          <span className="board-info-number emphasis">
            <span>{board_obj.matched_main_count}</span>
            <span className="board-info-plus">+</span>
            <span>{board_obj.matched_other_count}</span>
          </span>
        </div>
        <div>
          <span className="board-info-text">avg. combos</span>
          <span className="board-info-number emphasis">{board_obj.combo_count_avg.toFixed(1)}</span>
        </div>
        <div>
          <span className="board-info-text">avg. damage</span>
          <span className="board-info-number emphasis">x {board_obj.main_damage_multiplier_avg.toFixed(1)}</span>
        </div>
        <div>
          <span className="board-info-text">times of dropping</span>
          <span className="board-info-number emphasis">{board_obj.drop_times}</span>
        </div>
        <div>
          <span className="board-info-text">min. combos</span>
          <span className="board-info-number emphasis">{board_obj.combo_count_min}</span>
        </div>
      </div>,
      // infos.map(function(info) {
      //   return React.createElement("div", {className: "board-info"}, info);
      // }),
      React.createElement(Board, {board: board_obj.board, key: "board"}, null)
    ]);
  }
}

export class BoardCardsContainer extends React.Component {
  render() {
    return React.createElement("div", {className: "board-cards-container"},
      this.props.board_objs.map(function(board_obj, index) {
        let key = board_obj.board.join(" ");
        return React.createElement(BoardCard, {board_obj: board_obj, title: index+1, key: key}, null);
      })
    );
  }
}

// export default BoardCardsContainer;
