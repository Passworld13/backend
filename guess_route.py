from flask import Blueprint, request, jsonify
import json
import os

guess_bp = Blueprint('guess', __name__)
GAME_STATE_FILE = "game_state.json"

@guess_bp.route("/guess", methods=["POST"])
def guess_word():
    data = request.get_json()
    user_guess = data.get("guess")

    if not user_guess:
        return jsonify({"error": "Missing guess"}), 400

    if not os.path.exists(GAME_STATE_FILE):
        return jsonify({"error": "No game in progress"}), 400

    with open(GAME_STATE_FILE, "r") as f:
        game_state = json.load(f)

    correct_word = game_state.get("current_word")

    if user_guess.lower() == correct_word:
        response = {
            "result": "correct",
            "message": "🎉 Correct! You've guessed the word!",
            "word": correct_word,
            "pot_bonk": game_state.get("pot_bonk", 0)
        }
    else:
        game_state["fail_count"] += 1
        with open(GAME_STATE_FILE, "w") as f:
            json.dump(game_state, f)
        response = {
            "result": "incorrect",
            "message": "❌ Incorrect. Try again!",
            "fail_count": game_state["fail_count"]
        }

    return jsonify(response), 200

