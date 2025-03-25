import numpy as np 
class ConnectFour:
    def is_valid_move(self, board, col):
        # Checks if a move is valid:
        # - Column must be within bounds
        # - Top row of column must be empty
        return col >= 0 and col < len(board[0]) and board[0][col] == 0

    def drop_piece(self, board, col, player):
        print(f"Game board:\n{np.array(board)}")
        # Drops a player's piece into the specified column
        # Returns the row where it lands, or -1 if invalid
        for row in range(len(board) - 1, -1, -1):  # Start from bottom
            if board[row][col] == 0:
                board[row][col] = player  # Place the piece
                return row
        return -1  # Shouldn't happen if move was validated first

    def check_win(self, board, row, col, player):
        # Checks if the last move created a winning condition (4 in a row)
        # Returns (True, (start_row, start_col, end_row, end_col)) if win, False otherwise
        rows, cols = len(board), len(board[0])
        
        # Check horizontal
        count = 0
        start_col = end_col = col
        for c in range(cols):
            if board[row][c] == player:
                count += 1
                end_col = c
                if count == 4:
                    start_col = end_col - 3
                    return True, (row, start_col, row, end_col)
            else:
                count = 0

        # Check vertical
        count = 0
        start_row = end_row = row
        for r in range(rows):
            if board[r][col] == player:
                count += 1
                end_row = r
                if count == 4:
                    start_row = end_row - 3
                    return True, (start_row, col, end_row, col)
            else:
                count = 0

        # Check diagonal (top-left to bottom-right)
        count = 0
        r, c = row, col
        # Move to top-left of diagonal
        while r > 0 and c > 0:
            r -= 1
            c -= 1
        start_row, start_col = r, c
        # Count consecutive pieces along diagonal
        while r < rows and c < cols:
            if board[r][c] == player:
                count += 1
                end_row, end_col = r, c
                if count == 4:
                    start_row, start_col = end_row - 3, end_col - 3
                    return True, (start_row, start_col, end_row, end_col)
            else:
                count = 0
            r += 1
            c += 1

        # Check diagonal (top-right to bottom-left)
        count = 0
        r, c = row, col
        # Move to top-right of diagonal
        while r > 0 and c < cols - 1:
            r -= 1
            c += 1
        start_row, start_col = r, c
        # Count consecutive pieces along diagonal
        while r < rows and c >= 0:
            if board[r][c] == player:
                count += 1
                end_row, end_col = r, c
                if count == 4:
                    start_row, start_col = end_row - 3, end_col + 3
                    return True, (start_row, start_col, end_row, end_col)
            else:
                count = 0
            r += 1
            c -= 1

        return False  # No win found

    def is_board_full(self, board):
        # Checks if the board is completely filled
        return all(cell != 0 for row in board for cell in row)
