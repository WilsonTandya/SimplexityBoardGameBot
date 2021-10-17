import random
from time import time
import sys

sys.path.append('../../')

from src.utility import place
from src.constant import ColorConstant, GameConstant, ShapeConstant
from src.model import State, Player, Board

# from ..constant import ColorConstant, GameConstant, ShapeConstant
# from ..model import State,Player,Board,Piece
from typing import Tuple, List

from copy import deepcopy
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
        total_score = 0
        copy_state = deepcopy(state)
        board = copy_state.board
        is_placed = place(copy_state,n_player,shape,col) # returns -1 if invalid

        score_1 = score_2 = score_3 = score_4 = 0
        blank = ShapeConstant.BLANK

        if (is_placed != 1):
            for i in range(0, board.row):
                for j in range(0, board.col):
                    player_shape = shape
                    player_color = GameConstant.PLAYER_COLOR[n_player]
                   
                    # shape_1 = board[i][j].shape
                    # shape_2 = board[i+1][j].shape
                    # shape_3 = board[i+2][j].shape
                    # shape_4 = board[i+3][j].shape
                    # color_1 = board[i][j].color
                    # color_2 = board[i+1][j].color
                    # color_3 = board[i+2][j].color
                    # color_4 = board[i+3][j].color
                    try: 
                        shape_1 = board.__getitem__([i,j]).shape
                        shape_2 = board.__getitem__([i,j+1]).shape
                        shape_3 = board.__getitem__([i,j+2]).shape
                        shape_4 = board.__getitem__([i,j+3]).shape
                        color_1 = board.__getitem__([i,j]).color
                        color_2 = board.__getitem__([i,j+1]).color
                        color_3 = board.__getitem__([i,j+2]).color
                        color_4 = board.__getitem__([i,j+3]).color
                        # Garis dengan 1 bidak berdasarkan warna atau shape pemain: +1
                        # 1. X___
                        if (shape_2 == shape_3 == shape_4 == blank) and ((shape_1 == player_shape) or (color_1 == player_color)):
                            score_1 += 1
                        # 2. _X__
                        if (shape_1 == shape_3 == shape_4 == blank) and ((shape_2 == player_shape) or (color_2 == player_color)):
                            score_1 += 1
                        # 3. __X_
                        if (shape_1 == shape_2 == shape_4 == blank) and ((shape_3 == player_shape) or (color_3 == player_color)):
                            score_1 += 1
                        # 4. ___X
                        if (shape_1 == shape_2 == shape_3 == blank) and ((shape_4 == player_shape) or (color_4 == player_color)):
                            score_1 += 1

                        # Garis dengan 2 bidak berdasarkan warna pemain: +5
                        # 1. XX__
                        if (color_1 == color_2 == player_color) and (shape_3 == shape_4 == blank):
                            score_2 += 5
                        # 2. __XX
                        if (color_3 == color_4 == player_color) and (shape_1 == shape_2 == blank):
                            score_2 += 5
                        # 3. _X_X
                        if (color_2 == color_4 == player_color) and (shape_1 == shape_3 == blank):
                            score_2 += 5
                        # 4. X_X_
                        if (shape_2 == shape_4 == blank) and (color_1 == color_3 == player_color):
                            score_2 += 5
                        # 5. X__X
                        if (color_1 == color_4 == player_color) and (shape_2 == shape_3 == blank):
                            score_2 += 5
                        # 6. _XX_
                        if (shape_1 == shape_4 == blank) and (color_2 == color_3 == player_color):
                            score_2 += 5

                        # Garis dengan 2 bidak berdasarkan shape pemain: +10
                        # 1. XX__
                        if (shape_1 == shape_2 == player_shape) and (shape_3 == shape_4 == blank):
                            score_2 += 10
                        # 2. __XX
                        if (shape_3 == shape_4 == player_shape) and (shape_1 == shape_2 == blank):
                            score_2 += 10
                        # 3. _X_X
                        if (shape_2 == shape_4 == player_shape) and (shape_1 == shape_3 == blank):
                            score_2 += 10
                        # 4. X_X_
                        if (shape_2 == shape_4 == blank) and (shape_1 == shape_3 == player_shape):
                            score_2 += 10
                        # 5. X__X
                        if (shape_1 == shape_4 == player_shape) and (shape_2 == shape_3 == blank):
                            score_2 += 10
                        # 6. _XX_
                        if (shape_1 == shape_4 == blank) and (shape_2 == shape_3 == player_shape):
                            score_2 += 10
                        


                        # Garis dengan 3 bidak berdasarkan shape pemain: +50
                        # 1. XXX_
                        if (shape_1 == shape_2 == shape_3 == player_shape) and (shape_4 == blank):
                            score_3 += 50
                        # 2. XX_X 
                        if (shape_1 == shape_2 == shape_4 == player_shape) and (shape_3 == blank):
                            score_3 += 50
                        # 3. X_XX
                        if (shape_1 == shape_3 == shape_4 == player_shape) and (shape_2 == blank):
                            score_3 += 50
                        # 4. _XXX
                        if (shape_3 == shape_2 == shape_4 == player_shape) and (shape_1 == blank):
                            score_3 += 50
                        # Garis dengan 3 bidak berdasarkan warna pemain: +30
                        # 1. XXX_
                        if (color_1 == color_2 == color_3 == player_color) and (shape_4 == blank):
                            score_3 += 30
                        # 2. XX_X 
                        if (color_1 == color_2 == color_4 == player_color) and (shape_3 == blank):
                            score_3 += 30
                        # 3. X_XX
                        if (color_1 == color_3 == color_4 == player_color) and (shape_2 == blank):
                            score_3 += 30
                        # 4. _XXX
                        if (color_3 == color_2 == color_4 == player_color) and (shape_1 == blank):
                            score_3 += 30
                       
                        
                        # Garis dengan 4 bidak berdasarkan shape pemain: +1000
                        # Note: gausah dicek kanan kiri
                        if (shape_1 == shape_2 == shape_3 == shape_4 == player_shape):
                            score_4 += 1000
                        # Garis dengan 4 bidak berdasarkan warna pemain: +800
                        # Note: gausah dicek kanan kiri
                        if (color_1 == color_2 == color_3 == color_4 == player_color):
                            score_4 += 800
                        # 1000+800+30+50+5+1
                    except IndexError:
                        pass

        total_score = score_1 + score_2 + score_3 + score_4
        return total_score
    
    
    def vertical(state: State, n_player: int, shape: str, col: str) -> int:
        total_score = 0
        copy_state = deepcopy(state)
        board = copy_state.board
        is_placed = place(copy_state,n_player,shape,col) # returns -1 if invalid

        score_1 = score_2 = score_3 = score_4 = 0
        blank = ShapeConstant.BLANK

        if (is_placed != 1):
            for j in range (board.col):
                for i in range (board.row-1, -1, -1):
                    player_shape = shape
                    player_color = GameConstant.PLAYER_COLOR[n_player]

                    try:
                        shape_1 = board.__getitem__([i,j]).shape
                        shape_2 = board.__getitem__([i-1,j]).shape
                        shape_3 = board.__getitem__([i-2,j]).shape
                        shape_4 = board.__getitem__([i-3,j]).shape
                        color_1 = board.__getitem__([i,j]).color
                        color_2 = board.__getitem__([i-1,j]).color
                        color_3 = board.__getitem__([i-2,j]).color
                        color_4 = board.__getitem__([i-3,j]).color

                        # Pada ilustrasi di bawah, kiri = bawah, kanan = atas
                        # Garis dengan 1 bidak berdasarkan warna atau shape pemain: +1
                        # X___
                        if ((color_1 == player_color) or (shape_1 == player_shape)) and (shape_2 == shape_3 == shape_4 == blank):
                            score_1 += 1
                            
                        # Garis dengan 2 bidak berdasarkan warna pemain: +5
                        # XX__
                        if (color_1 == color_2 == player_color) and (shape_3 == shape_4 == blank):
                            score_2 += 5

                        # Garis dengan 2 bidak berdasarkan shape pemain: +10
                        # XX__
                        if (shape_1 == shape_2 == player_shape) and (shape_3 == shape_4 == blank):
                            score_2 += 10

                        # Garis dengan 3 bidak berdasarkan warna pemain: +30
                        # XXX_
                        if (color_1 == color_2 == color_3 == player_color) and (shape_4 == blank):
                            score_3 += 30

                        # Garis dengan 3 bidak berdasarkan shape pemain: +50
                        # XXX_
                        if (shape_1 == shape_2 == shape_3 == player_shape) and (shape_4 == blank):
                            score_3 += 50

                        # Garis dengan 4 bidak berdasarkan warna pemain: +800
                        if (color_1 == color_2 == color_3 == color_4 == player_color):
                            score_4 += 800

                        # Garis dengan 4 bidak berdasarkan shape pemain: +1000
                        if (shape_1 == shape_2 == shape_3 == shape_4 == player_shape):
                            score_4 += 1000

                    except IndexError:
                        pass

        total_score = score_1 + score_2 + score_3 + score_4
        return total_score


    def positive_diagonal(state: State, n_player: int, shape: str, col: str) -> int:
        total_score = 0
        state = deepcopy(state)
        board = state.board
        is_placed = place(state,n_player,shape,col) # returns -1 if invalid

        score_1 = score_2 = score_3 = score_4 = 0
        blank = ShapeConstant.BLANK
    
        if (is_placed != 1):
            for i in range(0, board.row):
                for j in range(0, board.col):
                    player_shape = shape
                    player_color = GameConstant.PLAYER_COLOR[n_player]
                    # shape_1 = board[i][j].shape
                    # shape_2 = board[i+1][j+1].shape
                    # shape_3 = board[i+2][j+2].shape
                    # shape_4 = board[i+3][j+3].shape
                    # color_1 = board[i][j].color
                    # color_2 = board[i+1][j+1].color
                    # color_3 = board[i+2][j+2].color
                    # color_4 = board[i+3][j+3].color
                    try: 
                        shape_1 = board.__getitem__([i,j]).shape
                        shape_2 = board.__getitem__([i+1,j+1]).shape
                        shape_3 = board.__getitem__([i+2,j+2]).shape
                        shape_4 = board.__getitem__([i+3,j+3]).shape
                        color_1 = board.__getitem__([i,j]).color
                        color_2 = board.__getitem__([i+1,j+1]).color
                        color_3 = board.__getitem__([i+2,j+2]).color
                        color_4 = board.__getitem__([i+3,j+3]).color
                        # Garis dengan 1 bidak berdasarkan warna atau shape pemain: +1
                        is_feasible = not j+3 > board.row
                        if (is_feasible):
                            # 1. X___
                            if  (shape_2 == shape_3 == shape_4 == blank) and ((shape_1 == player_shape) or (color_1 == player_color)):
                                score_1 += 1
                            # 2. _X__
                            if  (shape_1 == shape_3 == shape_4 == blank) and ((shape_2 == player_shape) or (color_2 == player_color)):
                                score_1 += 1
                            # 3. __X_
                            if  (shape_1 == shape_2 == shape_4 == blank) and ((shape_3 == player_shape) or (color_3 == player_color)):
                                score_1 += 1
                            # 4. ___X
                            if  (shape_1 == shape_2 == shape_3 == blank) and ((shape_4 == player_shape) or (color_4 == player_color)):
                                score_1 += 1

                            # Garis dengan 2 bidak berdasarkan warna pemain: +5
                            # 1. XX__
                            if  (color_1 == color_2 == player_color) and (shape_3 == shape_4 == blank):
                                score_2 += 5
                            # 2. __XX
                            if  (color_3 == color_4 == player_color) and (shape_1 == shape_2 == blank):
                                score_2 += 5
                            # 3. _X_X
                            if  (color_2 == color_4 == player_color) and (shape_1 == shape_3 == blank):
                                score_2 += 5
                            # 4. X_X_
                            if  (shape_2 == shape_4 == blank) and (color_1 == color_3 == player_color):
                                score_2 += 5
                            # 5. X__X
                            if  (color_1 == color_4 == player_color) and (shape_2 == shape_3 == blank):
                                score_2 += 5
                            # 6. _XX_
                            if  (shape_1 == shape_4 == blank) and (color_2 == color_3 == player_color):
                                score_2 += 5

                            # Garis dengan 2 bidak berdasarkan shape pemain: +10
                            # 1. XX__
                            if  (shape_1 == shape_2 == player_shape) and (shape_3 == shape_4 == blank):
                                score_2 += 10
                            # 2. __XX
                            if  (shape_3 == shape_4 == player_shape) and (shape_1 == shape_2 == blank):
                                score_2 += 10
                            # 3. _X_X
                            if  (shape_2 == shape_4 == player_shape) and (shape_1 == shape_3 == blank):
                                score_2 += 10
                            # 4. X_X_
                            if  (shape_2 == shape_4 == blank) and (shape_1 == shape_3 == player_shape):
                                score_2 += 10
                            # 5. X__X
                            if  (shape_1 == shape_4 == player_shape) and (shape_2 == shape_3 == blank):
                                score_2 += 10
                            # 6. _XX_
                            if  (shape_1 == shape_4 == blank) and (shape_2 == shape_3 == player_shape):
                                score_2 += 10
                            
                            # Garis dengan 3 bidak berdasarkan warna pemain: +30
                            # 1. XXX_
                            if  (color_1 == color_2 == color_3 == player_color) and (shape_4 == blank):
                                score_3 += 30
                            # 2. XX_X 
                            if  (color_1 == color_2 == color_4 == player_color) and (shape_3 == blank):
                                score_3 += 30
                            # 3. X_XX
                            if  (color_1 == color_3 == color_4 == player_color) and (shape_2 == blank):
                                score_3 += 30
                            # 4. _XXX
                            if (color_3 == color_2 == color_4 == player_color) and (shape_1 == blank):
                                score_3 += 30

                            # Garis dengan 3 bidak berdasarkan shape pemain: +50
                            # 1. XXX_
                            if  (shape_1 == shape_2 == shape_3 == player_shape) and (shape_4 == blank):
                                score_3 += 50
                            # 2. XX_X 
                            if  (shape_1 == shape_2 == shape_4 == player_shape) and (shape_3 == blank):
                                score_3 += 50
                            # 3. X_XX
                            if  (shape_1 == shape_3 == shape_4 == player_shape) and (shape_2 == blank):
                                score_3 += 50
                            # 4. _XXX
                            if  (shape_3 == shape_2 == shape_4 == player_shape) and (shape_1 == blank):
                                score_3 += 50

                            # Garis dengan 4 bidak berdasarkan warna pemain: +800
                            # Note: gausah dicek kanan kiri
                            if  (color_1 == color_2 == color_3 == color_4 == player_color):
                                score_4 += 800
                            
                            # Garis dengan 4 bidak berdasarkan shape pemain: +1000
                            # Note: gausah dicek kanan kiri
                            if  (shape_1 == shape_2 == shape_3 == shape_4 == player_shape):
                                score_4 += 1000
                    except IndexError:
                        pass
        print('score 1: '+str(score_1) +'\nscore 2:'+str(score_2)+'\nscore 3:'+str(score_3) +'\nscore 4:'+str(score_4))

        total_score = score_1 + score_2 + score_3 + score_4
        return total_score    

    def negative_diagonal(board: Board) -> int:
        pass

# TEST
test_board = Board(6,7)
# Misal player 1: cross red, player 2: circle blue
n_quota = 6 * 7 / 2

test_quota = [
    {
        ShapeConstant.CROSS: n_quota // 2,
        ShapeConstant.CIRCLE: n_quota - (n_quota // 2),
    },
    {
        ShapeConstant.CROSS: n_quota - (n_quota // 2),
        ShapeConstant.CIRCLE: n_quota // 2,
    },
]
test_players = [
            Player(
                ShapeConstant.CROSS, ColorConstant.RED, test_quota[0]
            ),
            Player(
                ShapeConstant.CIRCLE, ColorConstant.BLUE, test_quota[1]
            ),
        ]
test_state = State(test_board,test_players,1)
# place(test_state,0,"X",4)
# place(test_state,1,"O",3)
# place(test_state,0,"X",4)
# place(test_state,0,"X",4)
# place(test_state,0,"X",4)
place(test_state,0,"X",0)
place(test_state,0,"X",1)
place(test_state,0,"X",2)
place(test_state,0,"X",2)
# place(test_state,"X",3)

# minimax = Minimax()

# score = minimax.horizontal(1,"X","4")
# print(score)
# test_board.set_piece(5,3,'X')
# print(test_board)
# minimax = Minimax()
print(test_state.board)
score = Minimax.vertical(test_state,0,'O',2)
print(test_state.board)
print(score)
# score = minimax.horizontal(0,'X',3)
# print(score)