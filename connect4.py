def create_board():
    return [[0 for _ in range(7)] for _ in range(6)]

def print_board(board):
    for row in board:
        print("|", end=" ")
        for cell in row:
            if cell == 0:
                print(".", end=" ")
            elif cell == 1:
                print("X", end=" ")
            else:
                print("O", end=" ")
        print("|")
    print("+-+-+-+-+-+-+-+")
    print(" 0 1 2 3 4 5 6")

def is_valid_move(board, col):
    return col >= 0 and col < 7 and board[0][col] == 0

def drop_piece(board, col, player):
    for row in range(5, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    # Check horizontal
    count = 0
    for c in range(7):
        if board[row][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check vertical
    count = 0
    for r in range(6):
        if board[r][col] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0

    # Check diagonal (top-left to bottom-right)
    count = 0
    r, c = row, col
    while r > 0 and c > 0:
        r -= 1
        c -= 1
    while r < 6 and c < 7:
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
    while r > 0 and c < 6:
        r -= 1
        c += 1
    while r < 6 and c >= 0:
        if board[r][c] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        r += 1
        c -= 1

    return False

def is_board_full(board):
    return all(cell != 0 for row in board for cell in row)

def play_game():
    board = create_board()
    current_player = 1
    game_over = False

    print("Welcome to Connect 4!")
    print("Players take turns dropping pieces (X or O) into columns 0-6")

    while not game_over:
        print_board(board)
        move = input(f"Player {current_player} (X{'O' if current_player == 2 else ''}), choose a column (0-6): ")
        
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
                    current_player = 2 if current_player == 1 else 1
            else:
                print("Invalid move! Column is full or out of range.")
        except ValueError:
            print("Please enter a number between 0 and 6!")

if __name__ == "__main__":
    play_game()