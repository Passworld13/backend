from flask import Blueprint, request, jsonify
import os
import hashlib

guess_bp = Blueprint("guess", __name__)

# 🔐 Charger le mot depuis l'environnement (.env)
SECRET_WORD = os.getenv("SECRET_WORD", "defaultword").lower()

# 💥 Calculer et afficher le hash du mot du jour
hashed_word = hashlib.sha256(SECRET_WORD.encode()).hexdigest()
print(f"🔐 Hashed word of the day: {hashed_word}")

@guess_bp.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()

    if not data or "wallet" not in data or "word" not in data:
        return jsonify({"error": "Missing wallet or word"}), 400

    guess_word = data["word"].lower()

    if guess_word == SECRET_WORD:
        return jsonify({"result": "correct", "message": "You guessed the word!"})
    else:
        return jsonify({"result": "incorrect", "message": "Try again."})
