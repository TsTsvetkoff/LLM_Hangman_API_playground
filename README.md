# LLM_Hangman_API_playground

Hangman Game with Local LLM Integration

This project enables a local LLM to play Hangman via a custom API, using a Flask-based backend to manage the game state and a language model to make intelligent guesses.
Project Structure

    hangman_api.py: Flask API that hosts the Hangman game.
    local_llm.py: Code for interacting with the local LLM to make guesses.

Installation
````
Download your local llm and update its name in here https://github.com/TsTsvetkoff/LLM_Hangman_API_playground/blob/main/local_llm.py#L51
````

```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
Run the Hangman API:
```
python hangman_api.py
```
Run the LLM Interaction Script:

    python hangman_llm.py

API Endpoints

    /start: Starts a new game.
    /state: Returns current game state (word, guessed letters, attempts).
    /guess: Submits a guessed letter.

How It Works

    Hangman API: Manages game state and processes guesses.
    LLM Interaction: The LLM makes guesses based on the game state, with intelligent strategies like prioritizing vowels and common consonants.

Game Flow

    The game starts with an empty word (e.g., _ _ _ _).
    The LLM guesses letters based on the word display and guessed letters.
    The game continues until the word is completed or max wrong guesses are reached.
