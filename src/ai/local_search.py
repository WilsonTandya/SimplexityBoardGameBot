import random
from time import time
import copy
import math
from src.constant import ShapeConstant, GameConstant
from src.model import State,Board
from src.utility import place, is_out

from typing import Tuple, List


class LocalSearchGroup25:
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

    def evaluateState(self, board: Board, n_player) -> int :
        sum = 0
        #Bot = Player1
        if (n_player == 0) :
            for row in range(board.row):
                for col in range(board.col):
                    if(board[row, col].shape == GameConstant.PLAYER1_SHAPE or board[row, col].color == GameConstant.PLAYER1_COLOR) :
                        streak = self.checkMaxStreak(board, row, col)
                        sum += streak
                        if(board[row, col].shape == GameConstant.PLAYER1_SHAPE) : 
                            sum+=1
                        if(board[row, col].color == GameConstant.PLAYER1_COLOR) :
                            sum+=1
                    #Mengecek apakah move akan membuat musuh menang
                    if(board[row, col].shape == GameConstant.PLAYER2_SHAPE or board[row, col].color == GameConstant.PLAYER2_COLOR) :
                        streak = self.checkMaxStreak(board, row, col)
                        sum -= streak
        #Bot = Player2
        else :
            for row in range(board.row):
                for col in range(board.col):
                    if(board[row, col].shape == GameConstant.PLAYER2_SHAPE or board[row, col].color == GameConstant.PLAYER2_COLOR) :
                        streak = self.checkMaxStreak(board, row, col)
                        sum += streak
                        if(board[row, col].shape == GameConstant.PLAYER2_SHAPE) : 
                            sum+=1
                        if(board[row, col].color == GameConstant.PLAYER2_COLOR) :
                            sum+=1
                    #Mengecek apakah move akan membuat musuh menang
                    if(board[row, col].shape == GameConstant.PLAYER1_SHAPE or board[row, col].color == GameConstant.PLAYER1_COLOR) :
                        streak = self.checkMaxStreak(board, row, col)
                        sum -= streak
        return sum

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
        if(max_streak == 3) :
            max_streak = 9999
            
        return max_streak
    
    def prob(self, deltaE : int, thinking_time : float) -> float :
        try:
            return math.exp(deltaE/thinking_time)
        except OverflowError:
            return float('inf')
        

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.start_time = time()
        self.thinking_time = thinking_time 
        choosen_col, choosen_shape = (None, None)
        choosen_board = copy.deepcopy(state.board)
        while self.thinking_time > 0 :
            next_col, next_shape = self.randomNextMove(state)
            succ_board = self.randomNextSucc(state, n_player, next_shape, next_col)
            deltaE = self.evaluateState(succ_board, n_player) - self.evaluateState(choosen_board, n_player)
            if(deltaE > 0) :
                choosen_col, choosen_shape = next_col, next_shape
                choosen_board = succ_board
            else :
                if(self.prob(deltaE, self.thinking_time) > 0.8) :
                    choosen_col, choosen_shape = next_col, next_shape
                    choosen_board = succ_board
            self.thinking_time -= (time() - self.start_time)
        best_movement = choosen_col, choosen_shape
        return best_movement
