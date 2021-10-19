import random
from time import time
import sys

sys.path.append('../../')

from src.utility import place, is_win, is_full
from src.constant import ColorConstant, GameConstant, ShapeConstant
from src.model import State, Player, Board

from typing import Tuple, List

from copy import copy, deepcopy
class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        # best_movement = Minimax.minimax(state,n_player,True)
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        movements = Minimax.heuristic(state, n_player)
        random_number = random.randint(0,len(movements)-1)
        best_movement = movements[random_number][0]
        # best_movement = max(movements, key = lambda x: x[1])[0]
        alpha = -float("inf")
        beta = float("inf")
        value = Minimax.max_value(state, alpha, beta, n_player, 3)
        # print("value: ",value)

        # Look for movement in movements with heuristic = value
        found = False
        i = 0
        while(not found and i < len(movements)):
            if (movements[i][1] == value):
                found = True
                best_movement = movements[i][0]
            else:
                i += 1
        return best_movement

    # def minimax(state: State, n_player:int, alpha: int, beta: int, depth: int, maximizing_player: bool):
    #     movements = Minimax.heuristic(state, n_player)
    #     random_number = random.randint(0,len(movements)-1)
    #     best_movement = movements[random_number][0]
    #     board = state.board
    #     terminal_test = is_win(board) != None or is_full(board) or depth == 0

    #     if maximizing_player:
    #         value = -float("inf")
    #         for move in movements:
    #             score = Minimax.get_placement_score(state, n_player, move[0],)
    #     # best_movement = max(movements, key = lambda x: x[1])[0]
    #     alpha = -float("inf")
    #     beta = float("inf")
    #     if maximizing_player:
    #         value = Minimax.max_value(state, alpha, beta, n_player, 3)
    #     else:
    #         value = Minimax.min_value(state, alpha, beta, n_player, 3)
    #     # Look for movement in movements with heuristic = value
    #     found = False
    #     i = 0
    #     while(not found and i < len(movements)):
    #         if (movements[i][1] == value):
    #             found = True
    #             best_movement = movements[i][0]
    #         else:
    #             i += 1
    #     return best_movement

    def heuristic(state: State, n_player: int) -> Tuple[Tuple[str, str], int]:
        """
        Heuristic function to check heuristic value (objective function)

        [RETURN]
            Tuple[str, str] -> best movement
            int             -> heuristic value

        """
        # Array consists of movement possibilities with their heuristic value
        movement_heuristic = []
        copy_state = deepcopy(state)
        board = copy_state.board
        shapes = [GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER2_SHAPE] 
        for i in range(board.col):
            for j in range(len(shapes)):
                is_feasible = copy_state.players[n_player].quota[shapes[j]] != 0
                if (is_feasible):
                    score = Minimax.get_placement_score(copy_state,n_player,shapes[j],i)
                    movement = (i, shapes[j])
                    movement_heuristic.append((movement, score))
                    
        # for i in range (state.board.col):
        #     # Calculate for cross shape:
        #     # score = horizontal_streak + vertical_streak + positive_diagonal + negative_diagonal + minus
        #     # Set value in movement_heuristic array with score

        #     # Calculate for circle shape:
        #     # score = horizontal_streak + vertical_streak + positive_diagonal + negative_diagonal + minus
        #     # Set value in movement_heuristic array with score
        #     pass        
        # return max_heuristic, min_heuristic
        return movement_heuristic
    
    def get_possible_actions(state: State, n_player: int):
        # List all possible actions and result states
        actions = Minimax.heuristic(state, n_player)
        possible_actions = []
        result_states = []
        for a in actions:
            copy_state = deepcopy(state)
            if place(copy_state,n_player,a[0][1], a[0][0]) != -1:
                possible_actions.append((a[0][1], a[0][0]))
                result_states.append(copy_state)
        return possible_actions, result_states
    
    def max_value(state: State, alpha: int, beta: int, n_player: int, depth: int):
        board = deepcopy(state.board)
        terminal_test = is_win(board) != None or is_full(board) or depth == 0
        if (terminal_test):
            return Minimax.get_state_score(state, n_player)
        value = -float("inf")
        
        # List all possible actions
        possible_actions, result_states = Minimax.get_possible_actions(state, n_player)

        for i in range(len(possible_actions)):
            value = max(value, Minimax.min_value(result_states[i],alpha,beta,n_player,depth-1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value
    
    def min_value(state: State, alpha: int, beta: int, n_player: int, depth: int):
        board = deepcopy(state.board)
        terminal_test = is_win(board) != None or is_full(board) or depth == 0
        if (terminal_test):
            return Minimax.get_state_score(state, n_player) # menang atau engga
        value = float("inf")
        # List all possible actions
        possible_actions, result_states = Minimax.get_possible_actions(state, n_player)

        for i in range(len(possible_actions)):
            value = min(value, Minimax.max_value(result_states[i],alpha,beta,n_player,depth-1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def get_placement_score(state: State, n_player: int, shape: str, col: str) -> int:
        # Kondisi bisa nge place
        copy_state = deepcopy(state)
        place(copy_state, n_player, shape, col)
        score = Minimax.get_state_score(copy_state, n_player)
        return score

    def get_state_score(state: State, n_player:int) -> int:
        horizontal = Minimax.horizontal(state, n_player)
        vertical = Minimax.vertical(state, n_player)
        positive_diagonal = Minimax.positive_diagonal(state,n_player)
        negative_diagonal = Minimax.negative_diagonal(state, n_player)
        return horizontal + vertical + positive_diagonal + negative_diagonal

    def get_shape_color(n_player: int) -> Tuple[str,str,str,str]:
        if (n_player == 0):
            player_shape = GameConstant.PLAYER1_SHAPE
            player_color = GameConstant.PLAYER1_COLOR
            opponent_shape = GameConstant.PLAYER2_SHAPE
            opponent_color = GameConstant.PLAYER2_COLOR
        else:
            player_shape = GameConstant.PLAYER2_SHAPE
            player_color = GameConstant.PLAYER2_COLOR
            opponent_shape = GameConstant.PLAYER1_SHAPE
            opponent_color = GameConstant.PLAYER1_COLOR
        return player_shape, player_color, opponent_shape, opponent_color
    
    # Garis dengan 1 bidak berdasarkan warna atau shape pemain: +1
    # Garis dengan 2 bidak berdasarkan warna pemain: +5
    # Garis dengan 2 bidak berdasarkan shape pemain: +10
    # Garis dengan 3 bidak berdasarkan warna pemain: +30
    # Garis dengan 3 bidak berdasarkan shape pemain: +50
    # Garis dengan 4 bidak berdasarkan warna pemain: +800
    # Garis dengan 4 bidak berdasarkan shape pemain: +1000
    
    def horizontal(state: State, n_player: int) -> int:
        board = state.board
        score_1 = score_2 = score_3 = score_4 = 0
        blank = ShapeConstant.BLANK
        player_shape, player_color, opponent_shape, opponent_color = Minimax.get_shape_color(n_player)

        for i in range(0, board.row):
            for j in range(0, board.col):
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
                    if (shape_1 == shape_2 == shape_3 == shape_4 == player_shape):
                        score_4 += 1000
                    # Garis dengan 4 bidak berdasarkan warna pemain: +800
                    if (color_1 == color_2 == color_3 == color_4 == player_color):
                        score_4 += 800

                    # Cek opponent
                    # TODO 2 streak lawan minus juga atau engga?
                    # Garis dengan 2 bidak berdasarkan warna lawan: -5
                    # 1. XX__
                    if (color_1 == color_2 == opponent_color) and (shape_3 == shape_4 == blank):
                        score_2 -= 5
                    # 2. __XX
                    if (color_3 == color_4 == opponent_color) and (shape_1 == shape_2 == blank):
                        score_2 -= 5
                    # 3. _X_X
                    if (color_2 == color_4 == opponent_color) and (shape_1 == shape_3 == blank):
                        score_2 -= 5
                    # 4. X_X_
                    if (shape_2 == shape_4 == blank) and (color_1 == color_3 == opponent_color):
                        score_2 -= 5
                    # 5. X__X
                    if (color_1 == color_4 == opponent_color) and (shape_2 == shape_3 == blank):
                        score_2 -= 5
                    # 6. _XX_
                    if (shape_1 == shape_4 == blank) and (color_2 == color_3 == opponent_color):
                        score_2 -= 5

                    # Garis dengan 2 bidak berdasarkan shape lawan: -10
                    # 1. XX__
                    if (shape_1 == shape_2 == opponent_shape) and (shape_3 == shape_4 == blank):
                        score_2 -= 10
                    # 2. __XX
                    if (shape_3 == shape_4 == opponent_shape) and (shape_1 == shape_2 == blank):
                        score_2 -= 10
                    # 3. _X_X
                    if (shape_2 == shape_4 == opponent_shape) and (shape_1 == shape_3 == blank):
                        score_2 -= 10
                    # 4. X_X_
                    if (shape_2 == shape_4 == blank) and (shape_1 == shape_3 == opponent_shape):
                        score_2 -= 10
                    # 5. X__X
                    if (shape_1 == shape_4 == opponent_shape) and (shape_2 == shape_3 == blank):
                        score_2 -= 10
                    # 6. _XX_
                    if (shape_1 == shape_4 == blank) and (shape_2 == shape_3 == opponent_shape):
                        score_2 -= 10

                    # Garis dengan 3 bidak berdasarkan shape lawan: -50
                    # 1. XXX_
                    if (shape_1 == shape_2 == shape_3 == opponent_shape) and (shape_4 == blank):
                        score_3 -= 50
                    # 2. XX_X 
                    if (shape_1 == shape_2 == shape_4 == opponent_shape) and (shape_3 == blank):
                        score_3 -= 50
                    # 3. X_XX
                    if (shape_1 == shape_3 == shape_4 == opponent_shape) and (shape_2 == blank):
                        score_3 -= 50
                    # 4. _XXX
                    if (shape_3 == shape_2 == shape_4 == opponent_shape) and (shape_1 == blank):
                        score_3 -= 50
                    # Garis dengan 3 bidak berdasarkan warna lawan: -30
                    # 1. XXX_
                    if (color_1 == color_2 == color_3 == opponent_color) and (shape_4 == blank):
                        score_3 -= 30
                    # 2. XX_X 
                    if (color_1 == color_2 == color_4 == opponent_color) and (shape_3 == blank):
                        score_3 -= 30
                    # 3. X_XX
                    if (color_1 == color_3 == color_4 == opponent_color) and (shape_2 == blank):
                        score_3 -= 30
                    # 4. _XXX
                    if (color_3 == color_2 == color_4 == opponent_color) and (shape_1 == blank):
                        score_3 -= 30
                    
                    # Garis dengan 4 bidak berdasarkan shape lawan: -1000
                    if (shape_1 == shape_2 == shape_3 == shape_4 == opponent_shape):
                        score_4 -= 1000
                    # Garis dengan 4 bidak berdasarkan warna lawan: -800
                    if (color_1 == color_2 == color_3 == color_4 == opponent_color):
                        score_4 -= 800
                except IndexError:
                    pass

        total_score = score_1 + score_2 + score_3 + score_4
        # print("Horizontal: ",total_score)
        return total_score
    
    
    def vertical(state: State, n_player: int) -> int:
        board = state.board
        score_1 = score_2 = score_3 = score_4 = 0
        blank = ShapeConstant.BLANK
        player_shape, player_color, opponent_shape, opponent_color = Minimax.get_shape_color(n_player)

        for j in range (board.col):
            for i in range (board.row-1, -1, -1):
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

                    # CEK OPPONENT
                    # Garis dengan 2 bidak berdasarkan warna lawan: -5
                    # XX__
                    if (color_1 == color_2 == opponent_color) and (shape_3 == shape_4 == blank):
                        score_2 -= 5

                    # Garis dengan 2 bidak berdasarkan shape lawan: -10
                    # XX__
                    if (shape_1 == shape_2 == opponent_shape) and (shape_3 == shape_4 == blank):
                        score_2 -= 10

                    # Garis dengan 3 bidak berdasarkan warna lawan: -30
                    # XXX_
                    if (color_1 == color_2 == color_3 == opponent_color) and (shape_4 == blank):
                        score_3 -= 30

                    # Garis dengan 3 bidak berdasarkan shape lawan: -50
                    # XXX_
                    if (shape_1 == shape_2 == shape_3 == opponent_shape) and (shape_4 == blank):
                        score_3 -= 50

                    # Garis dengan 4 bidak berdasarkan warna lawan: -800
                    if (color_1 == color_2 == color_3 == color_4 == opponent_color):
                        score_4 -= 800

                    # Garis dengan 4 bidak berdasarkan shape lawan: -1000
                    if (shape_1 == shape_2 == shape_3 == shape_4 == opponent_shape):
                        score_4 -= 1000

                except IndexError:
                    pass

        total_score = score_1 + score_2 + score_3 + score_4
        # print("Vertical: ",total_score)
        return total_score


    def positive_diagonal(state: State, n_player: int) -> int:
        board = state.board
        score_1 = score_2 = score_3 = score_4 = 0
        blank = ShapeConstant.BLANK
        player_shape, player_color, opponent_shape, opponent_color = Minimax.get_shape_color(n_player)
    
        for i in range(0, board.row):
            for j in range(0, board.col):
                try: 
                    shape_1 = board.__getitem__([i,j]).shape
                    shape_2 = board.__getitem__([i+1,j-1]).shape
                    shape_3 = board.__getitem__([i+2,j-2]).shape
                    shape_4 = board.__getitem__([i+3,j-3]).shape
                    color_1 = board.__getitem__([i,j]).color
                    color_2 = board.__getitem__([i+1,j-1]).color
                    color_3 = board.__getitem__([i+2,j-2]).color
                    color_4 = board.__getitem__([i+3,j-3]).color
                  
                    is_feasible = not j-3 < 0 and not i+3 > board.row
                    if (is_feasible):
                        
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
                        if (shape_1 == shape_2 == shape_3 == shape_4 == player_shape):
                            score_4 += 1000
                        # Garis dengan 4 bidak berdasarkan warna pemain: +800
                        if (color_1 == color_2 == color_3 == color_4 == player_color):
                            score_4 += 800

                        # Cek opponent
                        # TODO 2 streak lawan minus juga atau engga?
                        # Garis dengan 2 bidak berdasarkan warna lawan: -5
                        # 1. XX__
                        if (color_1 == color_2 == opponent_color) and (shape_3 == shape_4 == blank):
                            score_2 -= 5
                        # 2. __XX
                        if (color_3 == color_4 == opponent_color) and (shape_1 == shape_2 == blank):
                            score_2 -= 5
                        # 3. _X_X
                        if (color_2 == color_4 == opponent_color) and (shape_1 == shape_3 == blank):
                            score_2 -= 5
                        # 4. X_X_
                        if (shape_2 == shape_4 == blank) and (color_1 == color_3 == opponent_color):
                            score_2 -= 5
                        # 5. X__X
                        if (color_1 == color_4 == opponent_color) and (shape_2 == shape_3 == blank):
                            score_2 -= 5
                        # 6. _XX_
                        if (shape_1 == shape_4 == blank) and (color_2 == color_3 == opponent_color):
                            score_2 -= 5

                        # Garis dengan 2 bidak berdasarkan shape lawan: -10
                        # 1. XX__
                        if (shape_1 == shape_2 == opponent_shape) and (shape_3 == shape_4 == blank):
                            score_2 -= 10
                        # 2. __XX
                        if (shape_3 == shape_4 == opponent_shape) and (shape_1 == shape_2 == blank):
                            score_2 -= 10
                        # 3. _X_X
                        if (shape_2 == shape_4 == opponent_shape) and (shape_1 == shape_3 == blank):
                            score_2 -= 10
                        # 4. X_X_
                        if (shape_2 == shape_4 == blank) and (shape_1 == shape_3 == opponent_shape):
                            score_2 -= 10
                        # 5. X__X
                        if (shape_1 == shape_4 == opponent_shape) and (shape_2 == shape_3 == blank):
                            score_2 -= 10
                        # 6. _XX_
                        if (shape_1 == shape_4 == blank) and (shape_2 == shape_3 == opponent_shape):
                            score_2 -= 10

                        # Garis dengan 3 bidak berdasarkan shape lawan: -50
                        # 1. XXX_
                        if (shape_1 == shape_2 == shape_3 == opponent_shape) and (shape_4 == blank):
                            score_3 -= 50
                        # 2. XX_X 
                        if (shape_1 == shape_2 == shape_4 == opponent_shape) and (shape_3 == blank):
                            score_3 -= 50
                        # 3. X_XX
                        if (shape_1 == shape_3 == shape_4 == opponent_shape) and (shape_2 == blank):
                            score_3 -= 50
                        # 4. _XXX
                        if (shape_3 == shape_2 == shape_4 == opponent_shape) and (shape_1 == blank):
                            score_3 -= 50
                        # Garis dengan 3 bidak berdasarkan warna lawan: -30
                        # 1. XXX_
                        if (color_1 == color_2 == color_3 == opponent_color) and (shape_4 == blank):
                            score_3 -= 30
                        # 2. XX_X 
                        if (color_1 == color_2 == color_4 == opponent_color) and (shape_3 == blank):
                            score_3 -= 30
                        # 3. X_XX
                        if (color_1 == color_3 == color_4 == opponent_color) and (shape_2 == blank):
                            score_3 -= 30
                        # 4. _XXX
                        if (color_3 == color_2 == color_4 == opponent_color) and (shape_1 == blank):
                            score_3 -= 30
                    
                        # Garis dengan 4 bidak berdasarkan shape lawan: -1000
                        if (shape_1 == shape_2 == shape_3 == shape_4 == opponent_shape):
                            score_4 -= 1000
                        # Garis dengan 4 bidak berdasarkan warna lawan: -800
                        if (color_1 == color_2 == color_3 == color_4 == opponent_color):
                            score_4 -= 800
                except IndexError:
                    pass
        total_score = score_1 + score_2 + score_3 + score_4
        # print("Positive diagonal: ", total_score)
        return total_score    


    def negative_diagonal(state: State, n_player: int) -> int:
        board = state.board
        score_1 = score_2 = score_3 = score_4 = 0
        blank = ShapeConstant.BLANK
        player_shape, player_color, opponent_shape, opponent_color = Minimax.get_shape_color(n_player)

        for i in range (board.row):
            for j in range (board.col):
                try:
                    shape_1 = board.__getitem__([i,j]).shape
                    shape_2 = board.__getitem__([i-1,j-1]).shape
                    shape_3 = board.__getitem__([i-2,j-2]).shape
                    shape_4 = board.__getitem__([i-3,j-3]).shape
                    color_1 = board.__getitem__([i,j]).color
                    color_2 = board.__getitem__([i-1,j-1]).color
                    color_3 = board.__getitem__([i-2,j-2]).color
                    color_4 = board.__getitem__([i-3,j-3]).color

                    is_feasible = not j-3 < 0 and not i-3 < 0
                    if(is_feasible):
                        # Pada ilustrasi di bawah, kanan = kanan bawah, kiri = kiri atas
                        # Garis dengan 1 bidak berdasarkan warna atau shape pemain: +1
                        # 1. ___X
                        if ((shape_1 == player_shape) or (color_1 == player_color)) and (shape_2 == shape_3 == shape_4 == blank):
                            score_1 += 1
                        # 2. __X_
                        if ((shape_2 == player_shape) or (color_2 == player_color)) and (shape_1 == shape_3 == shape_4 == blank):
                            score_1 += 1
                        # 3. _X__
                        if ((shape_3 == player_shape) or (color_3 == player_color)) and (shape_1 == shape_2 == shape_4 == blank):
                            score_1 += 1
                        # 4. X___
                        if ((shape_4 == player_shape) or (color_4 == player_color)) and (shape_1 == shape_2 == shape_3 == blank):
                            score_1 += 1

                        # Garis dengan 2 bidak berdasarkan warna pemain: +5
                        # 1. __XX
                        if (color_1 == color_2 == player_color) and (shape_3 == shape_4 == blank):
                            score_2 += 5
                        # 2. _X_X
                        if (color_1 == color_3 == player_color) and (shape_2 == shape_4 == blank):
                            score_2 += 5
                        # 3. X__X
                        if (color_1 == color_4 == player_color) and (shape_2 == shape_3 == blank):
                            score_2 += 5
                        # 4. _XX_
                        if (color_2 == color_3 == player_color) and (shape_1 == shape_4 == blank):
                            score_2 += 5
                        # 5. X_X_
                        if (color_2 == color_4 == player_color) and (shape_1 == shape_3 == blank):
                            score_2 += 5
                        # 6. XX__
                        if (color_3 == color_4 == player_color) and (shape_1 == shape_2 == blank):
                            score_2 += 5

                        # Garis dengan 2 bidak berdasarkan shape pemain: +10
                        # 1. __XX
                        if (shape_1 == shape_2 == player_shape) and (shape_3 == shape_4 == blank):
                            score_2 += 10
                        # 2. _X_X
                        if (shape_1 == shape_3 == player_shape) and (shape_2 == shape_4 == blank):
                            score_2 += 10
                        # 3. X__X
                        if (shape_1 == shape_4 == player_shape) and (shape_2 == shape_3 == blank):
                            score_2 += 10
                        # 4. _XX_
                        if (shape_2 == shape_3 == player_shape) and (shape_1 == shape_4 == blank):
                            score_2 += 10
                        # 5. X_X_
                        if (shape_2 == shape_4 == player_shape) and (shape_1 == shape_3 == blank):
                            score_2 += 10
                        # 6. XX__
                        if (shape_3 == shape_4 == player_shape) and (shape_1 == shape_2 == blank):
                            score_2 += 10

                        # Garis dengan 3 bidak berdasarkan warna pemain: +30
                        # 1. _XXX
                        if (color_1 == color_2 == color_3 == player_color) and (shape_4 == blank):
                            score_3 += 30
                        # 2. X_XX
                        if (color_1 == color_2 == color_4 == player_color) and (shape_3 == blank):
                            score_3 += 30
                        # 3. XX_X
                        if (color_1 == color_3 == color_4 == player_color) and (shape_2 == blank):
                            score_3 += 30
                        # 4. XXX_
                        if (color_2 == color_3 == color_4 == player_color) and (shape_1 == blank):
                            score_3 += 30

                        # Garis dengan 3 bidak berdasarkan shape pemain: +50
                        # 1. _XXX
                        if (shape_1 == shape_2 == shape_3 == player_shape) and (shape_4 == blank):
                            score_3 += 50
                        # 2. X_XX
                        if (shape_1 == shape_2 == shape_4 == player_shape) and (shape_3 == blank):
                            score_3 += 50
                        # 3. XX_X
                        if (shape_1 == shape_3 == shape_4 == player_shape) and (shape_2 == blank):
                            score_3 += 50
                        # 4. XXX_
                        if (shape_2 == shape_3 == shape_4 == player_shape) and (shape_1 == blank):
                            score_3 += 50

                        # Garis dengan 4 bidak berdasarkan warna pemain: +800
                        if (color_1 == color_2 == color_3 == color_4 == player_color):
                            score_4 += 800

                        # Garis dengan 4 bidak berdasarkan shape pemain: +1000
                        if (shape_1 == shape_2 == shape_3 == shape_4 == player_shape):
                            score_4 += 1000


                        # CEK OPPONENT
                        # Garis dengan 2 bidak berdasarkan warna lawan: -5
                        # 1. __XX
                        if (color_1 == color_2 == opponent_color) and (shape_3 == shape_4 == blank):
                            score_2 -= 5
                        # 2. _X_X
                        if (color_1 == color_3 == opponent_color) and (shape_2 == shape_4 == blank):
                            score_2 -= 5
                        # 3. X__X
                        if (color_1 == color_4 == opponent_color) and (shape_2 == shape_3 == blank):
                            score_2 -= 5
                        # 4. _XX_
                        if (color_2 == color_3 == opponent_color) and (shape_1 == shape_4 == blank):
                            score_2 -= 5
                        # 5. X_X_
                        if (color_2 == color_4 == opponent_color) and (shape_1 == shape_3 == blank):
                            score_2 -= 5
                        # 6. XX__
                        if (color_3 == color_4 == opponent_color) and (shape_1 == shape_2 == blank):
                            score_2 -= 5

                        # Garis dengan 2 bidak berdasarkan shape lawan: -10
                        # 1. __XX
                        if (shape_1 == shape_2 == opponent_shape) and (shape_3 == shape_4 == blank):
                            score_2 -= 10
                        # 2. _X_X
                        if (shape_1 == shape_3 == opponent_shape) and (shape_2 == shape_4 == blank):
                            score_2 -= 10
                        # 3. X__X
                        if (shape_1 == shape_4 == opponent_shape) and (shape_2 == shape_3 == blank):
                            score_2 -= 10
                        # 4. _XX_
                        if (shape_2 == shape_3 == opponent_shape) and (shape_1 == shape_4 == blank):
                            score_2 -= 10
                        # 5. X_X_
                        if (shape_2 == shape_4 == opponent_shape) and (shape_1 == shape_3 == blank):
                            score_2 -= 10
                        # 6. XX__
                        if (shape_3 == shape_4 == opponent_shape) and (shape_1 == shape_2 == blank):
                            score_2 -= 10

                        # Garis dengan 3 bidak berdasarkan warna lawan: -30
                        # 1. _XXX
                        if (color_1 == color_2 == color_3 == opponent_color) and (shape_4 == blank):
                            score_3 -= 30
                        # 2. X_XX
                        if (color_1 == color_2 == color_4 == opponent_color) and (shape_3 == blank):
                            score_3 -= 30
                        # 3. XX_X
                        if (color_1 == color_3 == color_4 == opponent_color) and (shape_2 == blank):
                            score_3 -= 30
                        # 4. XXX_
                        if (color_2 == color_3 == color_4 == opponent_color) and (shape_1 == blank):
                            score_3 -= 30

                        # Garis dengan 3 bidak berdasarkan shape lawan: -50
                        # 1. _XXX
                        if (shape_1 == shape_2 == shape_3 == opponent_shape) and (shape_4 == blank):
                            score_3 -= 50
                        # 2. X_XX
                        if (shape_1 == shape_2 == shape_4 == opponent_shape) and (shape_3 == blank):
                            score_3 -= 50
                        # 3. XX_X
                        if (shape_1 == shape_3 == shape_4 == opponent_shape) and (shape_2 == blank):
                            score_3 -= 50
                        # 4. XXX_
                        if (shape_2 == shape_3 == shape_4 == opponent_shape) and (shape_1 == blank):
                            score_3 -= 50

                        # Garis dengan 4 bidak berdasarkan warna lawan: -800
                        if (color_1 == color_2 == color_3 == color_4 == opponent_color):
                            score_4 -= 800

                        # Garis dengan 4 bidak berdasarkan shape lawan: -1000
                        if (shape_1 == shape_2 == shape_3 == shape_4 == opponent_shape):
                            score_4 -= 1000
                except IndexError:
                    pass

        total_score = score_1 + score_2 + score_3 + score_4
        # print("Negative diagonal: ",total_score)
        return total_score       

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
                ShapeConstant.CIRCLE, ColorConstant.RED, test_quota[0]
            ),
            Player(
                ShapeConstant.CROSS, ColorConstant.BLUE, test_quota[1]
            ),
        ]
test_state = State(test_board,test_players,1)


# Test Vertical
place(test_state,0,"O",0)
place(test_state,0,"O",1)
place(test_state,0,"O",2)
# # place(test_state,0,"O",2)
# # place(test_state,0,"O",1)
# # place(test_state,0,"O",2)
# # place(test_state,1,"X",6)
# # place(test_state,1,"X",6)

# print("TEST GET STATE SCORE\n")
# print(test_state.board)
# score = Minimax.get_placement_score(test_state,0,"O",3)
# print(score)

# # Test Positive Diagonal
# print("TEST POSITIVE DIAGONAL")
# print(test_state.board)
# score = Minimax.positive_diagonal(test_state,0,"X",2)   
# print(test_state.board)
# print(score)
# Score = 113 karena: 50+30+15+15+1+1+1 = 113

# # Test Positive Diagonal
# place(test_state,0,"X",0)

# Test Negative Diagonal
# place(test_state,0,"O",1)
# place(test_state,0,"O",1)
# place(test_state,0,"O",1)
# place(test_state,0,"O",2)
# place(test_state,0,"O",2)
# place(test_state,0,"X",3)
# place(test_state,1,"X",4)
# place(test_state,1,"X",4)
# place(test_state,1,"X",5)
# place(test_state,1,"X",5)

# print("TEST NEGATIVE DIAGONAL")
# print(test_state.board)
# score_neg_diag = Minimax.negative_diagonal(test_state,0,"X",3)
# score_ver = Minimax.vertical(test_state,0,"X",3)
# score_tot = score_neg_diag + score_ver
# print(str(score_neg_diag) + "+" + str(score_ver) + "=" + str(score_tot))