from flask import Flask, request, jsonify
import random

app = Flask(__name__)

WORDS = ["code", "play", "game", "hang", "test", "love", "chat", "node"]

game_state = {
    "word": "",
    "guessed_letters": [],
    "wrong_guesses": 0,
    "max_attempts": 15,
    "status": "ongoing",
}

def initialize_game():
    """Initialize a new Hangman game."""
    game_state["word"] = random.choice(WORDS)
    game_state["guessed_letters"] = []
    game_state["wrong_guesses"] = 0
    game_state["status"] = "ongoing"

def display_word(word, guessed_letters):
    """Return the current state of the word with guessed letters revealed."""
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

@app.route("/start", methods=["GET"])
def start_game():
    """Start a new game."""
    initialize_game()
    return jsonify({
        "message": "New game started!",
        "word_display": display_word(game_state["word"], game_state["guessed_letters"]),
        "max_attempts": game_state["max_attempts"],
    })

@app.route("/state", methods=["GET"])
def get_game_state():
    """Retrieve the current game state."""
    if game_state["status"] != "ongoing":
        return jsonify({
            "status": game_state["status"],
            "word": game_state["word"],
        })
    return jsonify({
        "word_display": display_word(game_state["word"], game_state["guessed_letters"]),
        "guessed_letters": game_state["guessed_letters"],
        "wrong_guesses": game_state["wrong_guesses"],
        "max_attempts": game_state["max_attempts"],
    })

@app.route("/guess", methods=["POST"])
def make_guess():
    """Process a guessed letter."""
    if game_state["status"] != "ongoing":
        return jsonify({"error": "Game is over. Start a new game."}), 400

    data = request.get_json()
    letter = data.get("letter", "").lower()

    if len(letter) != 1 or not letter.isalpha():
        return jsonify({"error": "Invalid guess. Please guess a single letter."}), 400

    if letter in game_state["guessed_letters"]:
        return jsonify({"error": "Letter already guessed."}), 400

    game_state["guessed_letters"].append(letter)
    if letter not in game_state["word"]:
        game_state["wrong_guesses"] += 1

    if set(game_state["word"]) <= set(game_state["guessed_letters"]):
        game_state["status"] = "won"
    elif game_state["wrong_guesses"] >= game_state["max_attempts"]:
        game_state["status"] = "lost"

    return jsonify({
        "word_display": display_word(game_state["word"], game_state["guessed_letters"]),
        "guessed_letters": game_state["guessed_letters"],
        "wrong_guesses": game_state["wrong_guesses"],
        "status": game_state["status"],
    })

if __name__ == "__main__":
    app.run(debug=True)
