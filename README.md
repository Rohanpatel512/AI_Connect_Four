# AI_Connect_Four
Presented by Group 23 of Winter 2025 CP468-C, this repository is our group's implementation of the Minimax algorithm and [Gemini's 1.5 Pro](https://ai.google.dev/gemini-api/docs/models#gemini-1.5-pro) model to solve an adversarial game of Connect 4.

## Setup and Install
To run the Python code, you must install [Git](https://git-scm.com/downloads) and [Python](https://www.python.org/).


1. Clone the repository:
```shell
git clone https://github.com/Rohanpatel512/AI_Connect_Four.git
```

2. Change to directory:
```shell
cd AI_Connect_Four
```

3. Install dependencies:
```shell
pip install -r requirements.txt
```

## Connecting the API
*Note: You will need a stable internet connection to connect to the Gemini API.*

4. a) Get a API key at [Google AI Studio](https://aistudio.google.com/):
   
    ![image](https://github.com/user-attachments/assets/844e1816-4920-4670-8ef1-25c71dae8083)

   b) Paste the key you generate into the key.json:
    ![image](https://github.com/user-attachments/assets/4806655c-4df2-45ca-aa13-0c634a664ec6)

## Running the Game

5. Run game_interface.py:
```shell
py game_interface.py
```

6. Select the model to use via textual input:

    ![image](https://github.com/user-attachments/assets/f02f2fc4-99c1-42b9-b6ba-c5c74a0c650e)

7. A Tkinter GUI should appear, simply select 'Start Game' to let the AI play.

    ![image](https://github.com/user-attachments/assets/49fa4915-a948-4fbe-bcef-b7c2224d82df)
    ![image](https://github.com/user-attachments/assets/ac9fd628-9352-4e8a-94db-a3eac5453230)
