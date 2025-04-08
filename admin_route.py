
from flask import Blueprint, request, jsonify
import json, os
from dotenv import load_dotenv

load_dotenv()
ADMIN_SECRET = os.getenv("ADMIN_SECRET")
GAME_STATE_FILE = "game_state.json"

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin/start_game", methods=["POST"])
def start_game():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Unauthorized"}), 401

    token = auth_header.split(" ")[1]
    if token != ADMIN_SECRET:
        return jsonify({"error": "Invalid token"}), 403

    data = request.get_json()
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
