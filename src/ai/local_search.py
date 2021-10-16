import random
from time import time
import copy
from src.constant import ShapeConstant, GameConstant
from src.model import State,Board
from src.utility import place, is_out

from typing import Tuple, List


class LocalSearch:
    def __init__(self):
        pass

    def randomNextSucc(self, state: State, n_player: int) :
        copy_state = copy.deepcopy(state)
        choosen_col, choosen_shape = (random.randint(0, copy_state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        while is_out(copy_state.board, 0, choosen_col) and choosen_shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE] :
            choosen_col, choosen_shape = (random.randint(0, copy_state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        placement = place(copy_state, n_player, choosen_shape, choosen_col)
        return copy_state.board
    
    def evaluateState(self, board: Board) -> int :
        max = 0
        for row in range(board.row):
            for col in range(board.col):
                if(board[row, col].shape == GameConstant.PLAYER1_SHAPE or board[row, col].color == GameConstant.PLAYER1_COLOR) :
                    streak = self.checkMaxStreak(board, row, col)
                    if(streak > max) :
                        max = streak
        return max

    def checkMaxStreak(self, board: Board, row: int, col: int) -> int :
        piece = board[row, col]
        if piece.shape == ShapeConstant.BLANK:
            return -1

        streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        max_streak = 0
        for prior in GameConstant.WIN_PRIOR:
            mark = 0
            for row_ax, col_ax in streak_way:
                row_ = row + row_ax
                col_ = col + col_ax
                for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                    if is_out(board, row_, col_) :
                        mark = 0
                        break

                    shape_condition = (
                        prior == GameConstant.SHAPE
                        and piece.shape != board[row_, col_].shape
                    )
                    color_condition = (
                        prior == GameConstant.COLOR
                        and piece.color != board[row_, col_].color
                    )
                    if shape_condition or color_condition:
                        break

                    row_ += row_ax
                    col_ += col_ax
                    mark += 1
                if mark > max_streak :
                    max_streak = mark
        return max_streak

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        for i in range(3) :
            succ_board = self.randomNextSucc(state, n_player)
            print("-------------------------State Awal----------------------------------")
            print(state.board)
            print("Nilai evaluasi : " + str(self.evaluateState(state.board)))
            print("-------------------------State Akhir----------------------------------")
            print(succ_board)
            print("Nilai evaluasi :" + str(self.evaluateState(succ_board)))

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        return best_movement