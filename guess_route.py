from flask import Blueprint, request, jsonify
import json
import os

GUESS_FILE = "game_state.json"

guess_bp = Blueprint('guess', __name__)

@guess_bp.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    user_guess = data.get("guess", "").strip().lower()

    if not os.path.exists(GUESS_FILE):
        return jsonify({"error": "Game not started yet"}), 400

    with open(GUESS_FILE, "r") as f:
        game_state = json.load(f)

    correct_word = game_state["current_word"]
    pot = game_state["pot_bonk"]
    price = game_state["guess_price_bonk"]

    if user_guess == correct_word:
        response = {
            "result": "correct",
            "message": f"🎉 Correct! The word was '{correct_word}'",
            "pot_bonk": pot
        }
        os.remove(GUESS_FILE)
        return jsonify(response), 200
    else:
        game_state["fail_count"] += 1
        game_state["pot_bonk"] += price
        with open(GUESS_FILE, "w") as f:
            json.dump(game_state, f)
        return jsonify({
            "result": "wrong",
            "message": "❌ Wrong guess. Try again.",
            "fail_count": game_state["fail_count"],
            "pot_bonk": game_state["pot_bonk"]
        }), 200

