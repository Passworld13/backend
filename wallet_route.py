from flask import Blueprint, jsonify

wallet_bp = Blueprint("wallet", __name__)

@wallet_bp.route("/connect_wallet", methods=["GET"])
def connect_wallet():
    return jsonify({"message": "Wallet connected successfully"})
