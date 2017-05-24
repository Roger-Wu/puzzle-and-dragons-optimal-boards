import React from 'react';
import { render } from 'react-dom';


class Board extends React.Component {
  render() {
    var rows = this.props.board.map(function(row_str) {
      var color_strs = row_str.split(' ');
      var row_orbs = color_strs.map(function(color_str) {
        return React.createElement('span', {className: 'orb orb-color-' + color_str}, null);
      });
      return React.createElement('div', {className: 'board-row'}, row_orbs);
    });
    return React.createElement('div', {className: 'board'}, rows);
  }
}

class BoardCard extends React.Component {
  render() {
    var board_obj = this.props.board_obj;
    var index = this.props.index;
    // var infos = [
    //   `${board_obj.combo_count} combos`,
    //   `${board_obj.main_combo_count} main combos`,
    //   `${board_obj.main_matched_count} matched main orbs`,
    //   `${board_obj.drop_times} times of dropping`,
    // ];
    var key = board_obj.board.join(' ');
    return React.createElement('div', {className: 'board-card', key: key}, [
      React.createElement('div', {className: 'board-index'}, `${index}`),
      <div className="board-info">
        <div>
          <span className="board-info-number board-info-combo emphasis">{board_obj.main_combo_count}+{board_obj.combo_count - board_obj.main_combo_count}</span>
          <span className="board-info-text"> combos</span>
        </div>
        <div>
          <span className="board-info-number emphasis">{board_obj.main_matched_count}</span>
          <span className="board-info-text"> matched main orbs</span>
        </div>
        <div>
          <span className="board-info-number emphasis">{board_obj.drop_times}</span>
          <span className="board-info-text"> times of dropping</span>
        </div>
      </div>,
      // infos.map(function(info) {
      //   return React.createElement('div', {className: 'board-info'}, info);
      // }),
      React.createElement(Board, {board: board_obj.board}, null)
    ]);
  }
}

class BoardCardsContainer extends React.Component {
  render() {
    return React.createElement('div', {className: 'board-cards-container'},
      this.props.board_objs.map(function(board_obj, index) {
        return React.createElement(BoardCard, {board_obj: board_obj, index: index+1}, null);
      })
    );
  }
}

export default BoardCardsContainer;