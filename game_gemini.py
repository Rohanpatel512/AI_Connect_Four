from google import genai
import json

def get_key(): # Literally just so I don't accidentally push the key out lol
    with open('key.json') as f:
        return json.load(f)

config = get_key()
API_KEY = config["api_key"]

def gemini_minimax(gemini_model_variant):
    # Creates Gemini client with API key
    client = genai.Client(api_key=API_KEY)

    # Generates a Connect 4 match based off of the prompt
    response = client.models.generate_content(
        model=gemini_model_variant,
        contents="""
        You will represent two players, Player 1 and Player 2 whom are playing 
        a game of Connect 4 against each other on a standard 7 section length 
        row, 6 section tall column gameboard. 

        Rules:
        The players may only play their checkers in one of the 7 columns (put 
        move results between 0-6).
        A player may not place a checker that exceeds the aforementioned board
        limits.
        The game only ends when a player places 4 checkers in a "row", which 
        can be arranged in an horizontal, vertical or diagonal line.

        Goal:
        Player 1 will try their best to win, whilst Player 2 actively tries to
        stop Player 1 for winning.

        Respond with each player's placement of checkers as two lists with each
        move being seperated by a single space for each designated player without 
        any additional text. Only respond with the players moves, with the only 
        distinction for who which list represents as a new line with a single '#'
        symbol.

        The game must end, therefore the output must have at least one winner or 
        tie via a full board.
        """
    )

    # Raw concat'd Gemini output
    print(f"Raw {gemini_model_variant} Output:")
    print(response.text)

    # Splits the results
    moves = response.text.split('#')
    player1 = moves[0].split()
    player2 = moves[1].split()

    # Console output
    print("Divided into lists (player movesets):")
    print("Player 1 moves:", player1)
    print("Player 2 moves:", player2)

    # Return the movesets
    return player1, player2