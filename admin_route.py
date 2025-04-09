
from flask import Blueprint, request, jsonify
import json
import os

GAME_STATE_FILE = "game_state.json"
ADMIN_PASSWORD = "secretpassword"

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin/start_game", methods=["POST"])
def start_game():
    data = request.get_json()

    if data.get("admin_password") != ADMIN_PASSWORD:
        return jsonify({"error": "Invalid password"}), 403

    word = data.get("word")
    hints = data.get("hints")

    if not word or not hints or len(hints) != 10:
        return jsonify({"error": "Word and exactly 10 hints are required"}), 400

    game_state = {
        "current_word": word.lower(),
        "hints": hints,
        "fail_count": 0,
        "guess_price_bonk": 100000,
        "pot_bonk": 0
    }

    with open(GAME_STATE_FILE, "w") as f:
        json.dump(game_state, f)

    return jsonify({"message": "Game started", "word": word, "hints": hints}), 200

@admin_bp.route("/admin/test")
def admin_test():
    return jsonify({"message": "Admin route OK"}), 200

