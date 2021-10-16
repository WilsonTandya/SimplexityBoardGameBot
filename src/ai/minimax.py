import random
from time import time

from src.constant import ColorConstant, ShapeConstant
from src.model import State

from typing import Tuple, List
from src.model import Board
from src.model import Piece
from copy import deepcopy
from utility import place
class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement

    def heuristic(state: State) -> Tuple[Tuple[str, str], int]:
        """
        Heuristic function to check heuristic value (objective function)

        [RETURN]
            Tuple[str, str] -> best movement
            int             -> heuristic value

        """
        # Array consists of movement possibilities with their heuristic value
        movement_heuristic = []

        for i in range (state.board.col):
            # Calculate for cross shape:
            # score = horizontal_streak + vertical_streak + positive_diagonal + negative_diagonal + minus
            # Set value in movement_heuristic array with score

            # Calculate for circle shape:
            # score = horizontal_streak + vertical_streak + positive_diagonal + negative_diagonal + minus
            # Set value in movement_heuristic array with score
            pass
        
        return movement_heuristic

    # Garis dengan 1 bidak berdasarkan warna atau shape pemain: +1
    # Garis dengan 2 bidak berdasarkan warna pemain: +5
    # Garis dengan 2 bidak berdasarkan shape pemain: +10
    # Garis dengan 3 bidak berdasarkan warna pemain: +30
    # Garis dengan 3 bidak berdasarkan shape pemain: +50
    # Garis dengan 4 bidak berdasarkan warna pemain: +800
    # Garis dengan 4 bidak berdasarkan shape pemain: +1000

    def horizontal(state: State, n_player: int, shape: str, col: str) -> int:
    # def horizontal(board: Board, piece: Tuple[str,str]) -> int:
        score = 0
        state = deepcopy(state)
        board = state.board
        place(state,n_player,shape,col)
        # board = deepcopy(board.board)
        # place 
        # if state.players[n_player].quota[shape] == 0:
        #     return -1

        # for row in range(board.row - 1, -1, -1):
        #     if board[row, col].shape == ShapeConstant.BLANK:
        #         piece = Piece(shape, GameConstant.PLAYER_COLOR[n_player])
        #         state.board.set_piece(row, col, piece)
        #         state.players[n_player].quota[shape] -= 1
        #         return row
# def place(state: State, n_player: int, shape: str, col: str) -> int:


        for i in range(0, board.row):
            for j in range(0, board.col):
                # Misal: player cross red, opponent circle blue
                # TODO mungkin perlu diganti colorconstant, shapeconstant sesuai shape pemain.
                player_shape = ShapeConstant.CROSS
                player_color = ColorConstant.RED
                blank = player_shape

                shape1 = board[i][j].shape
                shape2_right = board[i+1][j].shape
                shape3_right = board[i+2][j].shape
                shape4_right = board[i+3][j].shape
                shape2_left = board[i-1][j].shape
                shape3_left = board[i-2][j].shape
                shape4_left = board[i-3][j].shape
                color1 = board[i][j].color
                color2_right = board[i+1][j].color
                color3_right = board[i+2][j].color
                color4_right = board[i+3][j].color
                color2_left = board[i-1][j].color
                color3_left = board[i-2][j].color
                color4_left = board[i-3][j].color
                score_1 = score_2 = score_3 = score_4 = 0
                try: 
                    # Garis dengan 1 bidak berdasarkan warna atau shape pemain: +1
                    # 1. X___

                    # 2. _X__

                    # 3. __X_

                    # 4. ___X


                    # Garis dengan 2 bidak berdasarkan warna pemain: +5
                    # 1. XX__

                    # 2. __XX

                    # 3. _X_X

                    # 4. X_X_

                    # 5. X__X

                    # 6. _XX_

                    if (color1 == color2_right == color3_right) and (state[i+2][j].shape == state[i+3][j].shape == blank):
                        score_2 += 5

                    # Garis dengan 2 bidak berdasarkan shape pemain: +10
                    if (state[i][j].shape == state[i+1][j].shape == player_shape):
                        score += 10
                    
                    # Garis dengan 3 bidak berdasarkan warna pemain: +30
                    # 1. XXX_
                    if (color1 == color2_right == color3_right == player_color) and (color4_right == blank):
                        score_3 += 50
                    # 2. XX_X 
                    if (color1 == color2_right == color4_right == player_color) and (color3_right == blank):
                        score_3 += 50
                    # 3. X_XX
                    if (color1 == color3_right == color4_right == player_color) and (color2_right == blank):
                        score_3 += 50
                    # 4. _XXX
                    if (color3_right == color2_right == color4_right == player_color) and (color1 == blank):
                        score_3 += 50

                    # Garis dengan 3 bidak berdasarkan shape pemain: +50
                    # 1. XXX_
                    if (shape1 == shape2_right == shape3_right == player_shape) and (shape4_right == blank):
                        score_3 += 50
                    # 2. XX_X 
                    if (shape1 == shape2_right == shape4_right == player_shape) and (shape3_right == blank):
                        score_3 += 50
                    # 3. X_XX
                    if (shape1 == shape3_right == shape4_right == player_shape) and (shape2_right == blank):
                        score_3 += 50
                    # 4. _XXX
                    if (shape3_right == shape2_right == shape4_right == player_shape) and (shape1 == blank):
                        score_3 += 50

                    # Garis dengan 4 bidak berdasarkan warna pemain: +800
                    # Note: gausah dicek kanan kiri
                    if (color1 == color2_right == color3_right == color4_right == player_color):
                        score_4 += 1000
                    
                    # Garis dengan 4 bidak berdasarkan shape pemain: +1000
                    # Note: gausah dicek kanan kiri
                    if (shape1 == shape2_right == shape3_right == shape4_right == player_shape):
                        score_4 += 1000

                except IndexError:
                    pass
        total_score = score_1 + score_2 + score_3 + score_4
        return total_score
    
    
    def vertical(state: State, n_player: int, shape: str, col: str) -> int:
        score_1 = 0
        score_2 = 0
        score_3 = 0
        score_4 = 0

    def negative_diagonal(board: Board) -> int:
        pass
