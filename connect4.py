import tkinter as tk
from tkinter import messagebox

# Define grid dimensions as variables (can be changed here)
ROWS = 6  # Number of rows
COLS = 7  # Number of columns
CELL_SIZE = 80  # Size of each cell in pixels

def create_board(rows=ROWS, cols=COLS):
    # Creates an empty board with specified dimensions
    # 0 represents an empty cell
    return [[0 for _ in range(cols)] for _ in range(rows)]

class Connect4GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect 4")
        
        # Create game board
        self.board = create_board(ROWS, COLS)
        self.current_player = 1  # Player 1 starts
        
        # Create canvas for game board instead of console output
        self.canvas = tk.Canvas(master, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()
        
        # Draw grid and bind clicks instead of printing
        self.print_board()
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Add reset button
        self.reset_button = tk.Button(master, text="Reset Game", command=self.play_game)
        self.reset_button.pack(pady=10)

    def print_board(self):
        # Prints the current state of the game board (now draws to canvas)
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                
                # Draw pieces instead of text symbols
                if self.board[row][col] == 0:
                    pass  # Empty space (white rectangle is enough)
                elif self.board[row][col] == 1:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="red")
                else:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="yellow")

    def handle_click(self, event):
        # Handles mouse clicks instead of console input
        col = event.x // CELL_SIZE
        if self.is_valid_move(self.board, col):
            row = self.drop_piece(self.board, col, self.current_player)
            # Draw the board first to show the latest piece
            self.print_board()
            # Force the canvas to update and display the new piece
            self.canvas.update()
            
            win_result = self.check_win(self.board, row, col, self.current_player)
            if win_result:
                # Draw the winning line if there’s a win
                start_row, start_col, end_row, end_col = win_result[1]
                x1 = start_col * CELL_SIZE + CELL_SIZE // 2
                y1 = start_row * CELL_SIZE + CELL_SIZE // 2
                x2 = end_col * CELL_SIZE + CELL_SIZE // 2
                y2 = end_row * CELL_SIZE + CELL_SIZE // 2
                self.canvas.create_line(x1, y1, x2, y2, fill="black", width=3)
                self.canvas.update()
                
                winner = "Player 1 (Red)" if self.current_player == 1 else "Player 2 (Yellow)"
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.play_game()  # Reset instead of ending
            elif self.is_board_full(self.board):
                messagebox.showinfo("Game Over", "It's a tie!")
                self.play_game()  # Reset instead of ending
            else:
                # Switch players
                self.current_player = 2 if self.current_player == 1 else 1

    def is_valid_move(self, board, col):
        # Checks if a move is valid:
        # - Column must be within bounds
        # - Top row of column must be empty
        return col >= 0 and col < len(board[0]) and board[0][col] == 0

    def drop_piece(self, board, col, player):
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

    def play_game(self):
        # Main game loop (now resets the GUI game)
        self.board = create_board(ROWS, COLS)
        self.current_player = 1  # Player 1 starts
        self.print_board()

def main():
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()