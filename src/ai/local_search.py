import random
from time import time
import copy
import math
from src.constant import ShapeConstant, GameConstant
from src.model import State,Board
from src.utility import place, is_out

from typing import Tuple, List


class LocalSearch:
    def __init__(self):
        pass

    def randomNextMove(self, state: State) -> Tuple[str,str] :
        choosen_col, choosen_shape = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        while is_out(state.board, 0, choosen_col) and choosen_shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE] :
            choosen_col, choosen_shape = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE]))
        return choosen_col, choosen_shape

    def randomNextSucc(self, state: State, n_player: int, choosen_shape, choosen_col) :
        copy_state = copy.deepcopy(state)
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
    
    def prob(self, deltaE : int, thinking_time : float) -> float :
        return math.exp(deltaE/thinking_time)

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.start_time = time()
        self.thinking_time = thinking_time 
        choosen_col, choosen_shape = (None, None)
        print("-------------------------State Awal----------------------------------")
        print(state.board)
        print("Nilai evaluasi : " + str(self.evaluateState(state.board)))
        while self.thinking_time > 0 :
            next_col, next_shape = self.randomNextMove(state)
            succ_board = self.randomNextSucc(state, n_player, next_shape, next_col)
            deltaE = self.evaluateState(succ_board) > self.evaluateState(state.board)
            if(deltaE > 0) :
                choosen_col, choosen_shape = next_col, next_shape
            else :
                if(self.prob(deltaE, self.thinking_time) > 0.5) :
                    choosen_col, choosen_shape = next_col, next_shape
            print("-------------------------State Akhir----------------------------------")
            print(succ_board)
            print("Nilai evaluasi : " + str(self.evaluateState(succ_board)))
            self.thinking_time -= (time() - self.start_time)
        best_movement = choosen_col, choosen_shape
        return best_movement

# print("-------------------------State Awal----------------------------------")
# print(state.board)
# print("Nilai evaluasi : " + str(self.evaluateState(state.board)))
# print("-------------------------State Akhir----------------------------------")
# print(succ_board)
# print("Nilai evaluasi : " + str(self.evaluateState(succ_board)))