# Define grid dimensions as variables (can be changed here)
ROWS = 6  # Number of rows
COLS = 7  # Number of columns

def create_board(rows=ROWS, cols=COLS):
    # Creates an empty board with specified dimensions
    # 0 represents an empty cell
    return [[0 for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Prints the current state of the game board
    for row in board:
        print("|", end=" ")  # Left border of each row
        for cell in row:
            # Display appropriate symbol based on cell value
            if cell == 0:
                print(".", end=" ")  # Empty space
            elif cell == 1:
                print("X", end=" ")  # Player 1's piece
            else:
                print("O", end=" ")  # Player 2's piece
        print("|")  # Right border of each row
    
    # Print column numbers below the board
    print("+" + "-+" * len(board[0]))  # Bottom border
    print(" ", end=" ")
    for i in range(len(board[0])):
        print(i, end=" ")  # Column numbers
    print()

def is_valid_move(board, col):
    # Checks if a move is valid:
    # - Column must be within bounds
    # - Top row of column must be empty
    return col >= 0 and col < len(board[0]) and board[0][col] == 0

def drop_piece(board, col, player):
    # Drops a player's piece into the specified column
    # Returns the row where it lands, or -1 if invalid
    for row in range(len(board) - 1, -1, -1):  # Start from bottom
        if board[row][col] == 0:
            board[row][col] = player  # Place the piece
            return row
    return -1  # Shouldn't happen if move was validated first

def check_win(board, row, col, player):
    # Checks if the last move created a winning condition (4 in a row)
    rows, cols = len(board), len(board[0])
    
    # Check horizontal
    count = 0
    for c in range(cols):
        if board[row][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(rows):
        if board[r][col] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    r, c = row, col
    # Move to top-left of diagonal
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    # Count consecutive pieces along diagonal
    while r < rows and c < cols:
        if board[r][c] == player:
            count += 1
            if count == 4:
                return True
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
    # Count consecutive pieces along diagonal
    while r < rows and c >= 0:
        if board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c -= 1

    return False  # No win found

def is_board_full(board):
    # Checks if the board is completely filled
    return all(cell != 0 for row in board for cell in row)

def play_game():
    # Main game loop
    board = create_board(ROWS, COLS)
    current_player = 1  # Player 1 starts
    game_over = False

    # Welcome message
    print("Welcome to Connect 4!")
    print(f"Players take turns dropping pieces (X or O) into columns 0-{COLS-1}")

    while not game_over:
        print_board(board)
        # Get player input
        move = input(f"Player {current_player} (X{'O' if current_player == 2 else ''}), choose a column (0-{COLS-1}): ")
        
        try:
            col = int(move)
            if is_valid_move(board, col):
                row = drop_piece(board, col, current_player)
                if check_win(board, row, col, current_player):
                    print_board(board)
                    print(f"Player {current_player} wins!")
                    game_over = True
                elif is_board_full(board):
                    print_board(board)
                    print("It's a tie!")
                    game_over = True
                else:
                    # Switch players
                    current_player = 2 if current_player == 1 else 1
            else:
                print(f"Invalid move! Column must be 0-{COLS-1} and not full.")
        except ValueError:
            print(f"Please enter a number between 0 and {COLS-1}!")

if __name__ == "__main__":
    play_game()