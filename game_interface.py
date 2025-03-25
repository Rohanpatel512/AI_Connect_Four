import tkinter as tk
import random # random move for tie case
from tkinter import messagebox
from game import ConnectFour
from game_ai import AI_player
from game_gemini import gemini_minimax
import numpy as np

# Define grid dimensions as variables (can be changed here)
ROWS = 6  # Number of rows
COLS = 7  # Number of columns
CELL_SIZE = 80  # Size of each cell in pixels

def create_board(rows=ROWS, cols=COLS):
    # Creates an empty board with specified dimensions
    # 0 represents an empty cell
    return [[0 for _ in range(cols)] for _ in range(rows)]

class Connect4GUI:
    def __init__(self, master, model):
        self.game = ConnectFour()
        self.master = master
        self.master.title("Connect 4")

        # Model to play against
        self.model = model
        
        # Create game board
        self.board = create_board(ROWS, COLS)
        self.current_player = 1  # Flag indicating which player starts (AI player 1 starts)
        self.ai_player1 = AI_player() # Player 1 (AI player)
        self.ai_player2 = AI_player() # Player 2 (AI Player)
        
        # Create canvas for game board instead of console output
        self.canvas = tk.Canvas(master, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()

        self.print_board()
        
        # Add reset button
        self.reset_button = tk.Button(master, text="Reset Game", command=self.play_game)
        self.start_button = tk.Button(master, text="Start Game", command=self.start_game)
        self.reset_button.pack(pady=10)
        self.start_button.pack(pady=5, padx=10)

    
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
    
    def draw_piece(self, row, col, color):
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        #self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")   

        # Draw pieces instead of text symbols
        if self.board[row][col] == 0:
            pass  # Empty space (white rectangle is enough)
        elif self.board[row][col] == 1:
            self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="red")
        elif self.board[row][col] == 2:
            self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="blue")
    
    def start_game(self):
        if self.model != "minimax":
            try:
                max_gemini_output, min_gemini_output = gemini_minimax(self.model)
            except Exception as e:
                print("Error with Gemini Minimax!\nException:", e)

        round = 0
        while self.game.is_board_full(self.board) == False: # While the board is not full 
            print("Turn:", round)
            if self.current_player == 1:
                # Max's turn
                if self.model == "minimax": _, col = self.ai_player1.minimax(self.game, self.board, 6, float('-inf'), float('inf'), True)
                else: 
                    try: col = int(max_gemini_output[round])
                    except Exception as e:
                        print(e)
                        break
                print("Player 1 played:", col)
                row = self.game.drop_piece(self.board, col, self.current_player)
                self.draw_piece(row, col, "red")
                self.canvas.update()
                
                # Check for victory and display message box if player 1 (max) is victorious
                isWin = self.display_win(row, col)
                if isWin:
                    winner = "Player 1 (Red)"
                    print("Game Over", f"{winner} wins!")
                    messagebox.showinfo("Game Over", f"{winner} wins!")
                    break

                # Switch players turn 
                self.current_player = 2
            else:
                # Min's turn 
                if self.model == "minimax": _, col = self.ai_player2.minimax(self.game, self.board, 6, float('-inf'), float('inf'), False)
                else: 
                    try: col = int(min_gemini_output[round])
                    except Exception as e:
                        print(e)
                        break
                print("Player 2 played:", col)
                row = self.game.drop_piece(self.board, col, self.current_player)
                self.draw_piece(row, col, "blue")
                self.canvas.update()

                # Check for victory and display message box if player 2 (min) is victorious
                isWin = self.display_win(row, col)
                if isWin:
                    winner = "Player 2 (Blue)"
                    print("Game Over", f"{winner} wins!")
                    messagebox.showinfo("Game Over", f"{winner} wins!")
                    break

                # Switch players turn 
                self.current_player = 1

                # Both players have played, so onto the next round
                round += 1

    def display_win(self, row, col):
        win_result = self.game.check_win(self.board, row, col, self.current_player)
        if win_result:
            # Draw the winning line if there’s a win
            start_row, start_col, end_row, end_col = win_result[1]
            x1 = start_col * CELL_SIZE + CELL_SIZE // 2
            y1 = start_row * CELL_SIZE + CELL_SIZE // 2
            x2 = end_col * CELL_SIZE + CELL_SIZE // 2
            y2 = end_row * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=3)
            self.canvas.update()
            
            return True 

        return False

    def play_game(self):
        # Main game loop (now resets the GUI game)
        self.board = create_board(ROWS, COLS)
        self.current_player = 1  # Player 1 starts
        self.print_board()

def main():
    # Model selection
    selection = input("""CP468 Group 23 - Connect 4
Please input the model you would like to use:
minimax (m) - Our own written Minimax algorithm
gemini  (g) - By default uses Gemini 1.5 Pro
custom  (c) - A custom Gemini model variant you want to use

Input: """)

    selection = selection.lower()

    if selection == "m" or selection == "minimax":
        model = "minimax"
    elif selection == "g" or selection == "gemini":
        model = "gemini-1.5-pro" # Default Gemini model variant
    elif selection == "c" or selection == "custom":
        model = input("\nPlease input the Gemini model variant you would like to work with.\nMake sure your input is in kebab case (ie. gemini-2.0-flash for Gemini 2.0 Flash)!\n\n")
    else:
        model = "minimax" # Default
    
    root = tk.Tk() # GUI
    app = Connect4GUI(root, model)
    root.mainloop()

if __name__ == "__main__":
    main()