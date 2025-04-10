from flask import Blueprint, request, jsonify
import json
import os

link_bp = Blueprint("link", __name__)
LINKED_WALLETS_FILE = "linked_wallets.json"
SESSIONS_FILE = "sessions.json"

@link_bp.route("/link_wallet", methods=["POST"])
def link_wallet():
    data = request.get_json()
    session_id = data.get("session_id")
    wallet_address = data.get("wallet_address")

    # Load sessions
    if not os.path.exists(SESSIONS_FILE):
        return jsonify({"error": "No session file found"}), 400

    with open(SESSIONS_FILE, "r") as f:
        sessions = json.load(f)

    if session_id not in sessions:
        return jsonify({"error": "Invalid or expired session"}), 403

    telegram_id = sessions[session_id]

    # Load existing links
    if os.path.exists(LINKED_WALLETS_FILE):
        with open(LINKED_WALLETS_FILE, "r") as f:
            links = json.load(f)
    else:
        links = {}

    links[str(telegram_id)] = wallet_address

    with open(LINKED_WALLETS_FILE, "w") as f:
        json.dump(links, f, indent=2)

    # Optionally: delete session after use
    del sessions[session_id]
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f)

    return jsonify({"message": "Wallet linked successfully!"}), 200

