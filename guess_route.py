from flask import Blueprint, request, jsonify

guess_bp = Blueprint("guess", __name__)

# Exemple simple : le mot du jour est en dur ici
SECRET_WORD = "pain"

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
