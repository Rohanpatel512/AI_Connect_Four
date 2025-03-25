# Imports
import random
import copy 

# Constants
ROWS = 6
COLS = 7
CELL_SIZE = 80

class AI_player:

    def evaluate_board(self, game, board, player):
        # basic evl function: prior center, block opponent and win
        opponent = 1 if player == 2 else 2
        score = 0
        
        # prior center column
        center_col = COLS // 2
        center_count = sum([1 for row in range(ROWS) if board[row][center_col] == player])
        score += center_count * 3
        
        # check for w/l conditions
        if any(game.check_win(board, row, col, player) for row in range(ROWS) for col in range(COLS)):
            return 1000
        if any(game.check_win(board, row, col, opponent) for row in range(ROWS) for col in range(COLS)):
            return -1000
        
        return score

    def minimax(self, game, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.is_board_full(board):
            return self.evaluate_board(game, board, 2 if maximizing_player else 1), None
        valid_moves = [col for col in range(COLS) if game.is_valid_move(board, col)]
        if maximizing_player:
            max_eval = float('-inf')
            for col in valid_moves:
                temp_board = copy.deepcopy(board)
                row = game.drop_piece(temp_board, col, 2)

                eval_score, _ = self.minimax(game, temp_board, depth - 1, alpha, beta, False)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval = float('inf')
            for col in valid_moves:
                temp_board = copy.deepcopy(board)
                row = game.drop_piece(temp_board, col, 1)
                eval_score, _ = self.minimax(game, temp_board, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move