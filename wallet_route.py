from flask import Blueprint, request, jsonify
import json
import os

wallet_bp = Blueprint("wallet", __name__)
WALLET_DB = "wallets.json"

def save_wallet(session, wallet):
    if os.path.exists(WALLET_DB):
        with open(WALLET_DB, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[session] = wallet

    with open(WALLET_DB, "w") as f:
        json.dump(data, f, indent=2)

@wallet_bp.route("/wallet", methods=["POST"])
def link_wallet():
    payload = request.json
    session = payload.get("session")
    wallet = payload.get("wallet")

    if not session or not wallet:
        return jsonify({"error": "Missing session or wallet"}), 400

    save_wallet(session, wallet)
    return jsonify({"status": "Wallet linked", "wallet": wallet})
