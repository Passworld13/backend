from flask import Blueprint, request, jsonify
import json
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

guess_bp = Blueprint("guess", __name__)

BONK_TOKEN = os.getenv("BONK_TOKEN")
WALLET_GAME = os.getenv("WALLET_GAME")
WALLET_FOUNDER = os.getenv("WALLET_FOUNDER")
WALLET_TREASURY = os.getenv("WALLET_TREASURY")
WALLET_BURN = os.getenv("WALLET_BURN")

POT_FILE = "pot.json"

def get_pot():
    with open(POT_FILE, "r") as f:
        return json.load(f)

def update_pot(data):
    with open(POT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def transfer_bonk(from_wallet, to_wallet, amount):
    print(f"Transfer {amount} BONK from {from_wallet} to {to_wallet}")
    return True

def hash_word(word):
    return hashlib.md5(word.encode()).hexdigest()

@guess_bp.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    telegram_user = data.get("telegram_user")
    wallet = data.get("wallet")
    guess_word = data.get("guess")

    if not all([telegram_user, wallet, guess_word]):
        return jsonify({"error": "Missing fields"}), 400

    pot = get_pot()
    pot["guess_count"] += 1
    pot["guesses"].append({"user": telegram_user, "guess": guess_word})

    if hash_word(guess_word.lower()) == pot["word_hash"]:
        amount = pot["pot_bonk"]
        transfer_bonk(WALLET_GAME, wallet, amount)
        pot["pot_bonk"] = 0
        pot["guess_count"] = 0
        pot["guesses"] = []
        pot["word_hash"] = ""
        update_pot(pot)
        return jsonify({"status": "correct", "reward": amount})

    price = pot["guess_price"]
    transfer_bonk(wallet, WALLET_GAME, price)

    pot["pot_bonk"] += int(price * 0.70)
    transfer_bonk(wallet, WALLET_FOUNDER, int(price * 0.15))
    transfer_bonk(wallet, WALLET_TREASURY, int(price * 0.10))
    transfer_bonk(wallet, WALLET_BURN, int(price * 0.05))

    if pot["guess_count"] % 50 == 0:
        pot["guess_price"] = int(pot["guess_price"] * 2)

    update_pot(pot)
    return jsonify({"status": "incorrect", "new_pot": pot["pot_bonk"], "price": pot["guess_price"]})
