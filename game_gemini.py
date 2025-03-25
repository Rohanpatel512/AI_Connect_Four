from google import genai
import json

def get_key(): # literally just so I don't push the key out lol
    with open('key.json') as f:
        return json.load(f)

config = get_key()
API_KEY = config["api_key"]

client = genai.Client(api_key=API_KEY) # creates our Gemini client

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="""
    You will represent two players, Player 1 and Player 2 whom are playing 
    a game of Connect 4 on a standard 7 section length row, 6 section tall 
    column gameboard. Respond only with each player's moves in the format:

    Player: (player number)
    Dropped: (column number)

    When the game concludes, output the result in the following format:

    Winner: (player number)
    Gameboard: 
    (generated connect 4 gameboard in ASCII characters)
    """
)

print(response.text)