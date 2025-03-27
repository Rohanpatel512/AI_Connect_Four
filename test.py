from google import genai
import json

def get_key(): # Literally just so I don't accidentally push the key out
    with open('key.json') as f:
        return json.load(f)

config = get_key()
API_KEY = config["api_key"]

client = genai.Client(api_key=API_KEY)

def gemini_init_max(model):
    # MAXIMUM
    MAX_PROMPT = """"
You are playing a game of Connect Four on a standard 7 section length 
row, 6 section tall column gameboard. Your checkers are represented as
the number 1.

Rules:
The players may only play their checkers in one of the 7 columns (put 
move results between 0-6).
You may NOT place a checker on a column that is full.
The game only ends when a player places 4 checkers in a "row", which 
can be arranged in an horizontal, vertical or diagonal line.

Goal:
You are trying to win the game, as such, respond with the best move by 
responding with ONLY the column number to play that will maximize your 
chances of success.

A new board will be sent with the opponent's move, the game will
conclude once the game is won. You will be going first, so please 
select a column to start.

For all future moves, choose on a column that is not full.
Respond ONLY with the column number. 
"""

    # Initial max prompt and history initialization
    max_conversation_history = []
    max_conversation_history.append({"role": "user", "content": MAX_PROMPT}) # Add prompt to history
    response = client.models.generate_content(
        model=model,
        contents=MAX_PROMPT
    )
    max_conversation_history.append({"role": "model", "content": response.text}) # Add response to history

    return max_conversation_history, int(max_conversation_history[1]["content"])

def gemini_init_min(board, model):
    # MINIMUM PROMPT
    MIN_PROMPT = f""""
You are playing a game of Connect Four on a standard 7 section length 
row, 6 section tall column gameboard. Your checkers are represented as
the number 2.

Rules:
The players may only play their checkers in one of the 7 columns (put 
move results between 0-6).
You may NOT place a checker on a column that is full.
The game only ends when a player places 4 checkers in a "row", which 
can be arranged in an horizontal, vertical or diagonal line.

Goal:
You are trying to prevent the other player from winning the game, as 
such, respond with the best move by responding with ONLY the column 
number to play that will maximize your chances of decreasing their
success.

A new board will be sent with the opponent's move, the game will
conclude once the game is won. Here is the current board:
{board}

For all future moves, choose on a column that is not full. 
Respond ONLY with the column number. 
"""

    # Initial min prompt and history initialization
    min_conversation_history = []
    min_conversation_history.append({"role": "user", "content": MIN_PROMPT}) # Add prompt to history
    response = client.models.generate_content(
        model=model,
        contents=MIN_PROMPT
    )
    min_conversation_history.append({"role": "model", "content": response.text}) # Add response to history

    return min_conversation_history, int(min_conversation_history[1]["content"])

def gemini_move(conversation_history, board, model):
    # Sends gameboard and chat history to Gemini
    prompt = ""
    for turn in conversation_history:
        prompt += f"{turn['role']}: {turn['content']}\n"
    prompt += f"gameboard: {board}\n"
    
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    print("Move:", response.text)
    conversation_history.append({"role": "user", "content": prompt})
    conversation_history.append({"role": "model", "content": response.text})

    print(conversation_history[-1]["content"])
    return conversation_history, int(conversation_history[-1]["content"])