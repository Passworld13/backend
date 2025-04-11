from flask import Blueprint, request, render_template, jsonify
from flask_cors import CORS

wallet_connect_bp = Blueprint("wallet_connect", __name__)
CORS(wallet_connect_bp)  # pour autoriser les requêtes du frontend

@wallet_connect_bp.route("/")
def index():
    return "Passworld backend is alive"

@wallet_connect_bp.route("/connect")
def connect_wallet():
    tg_id = request.args.get("tg_id")
    return render_template("wallet_connect.html", tg_id=tg_id)

@wallet_connect_bp.route("/verify", methods=["POST"])
def verify_signature():
    data = request.json
    # TODO : Ajouter la vérification de signature ici
    return jsonify({"status": "success", "wallet": data.get("address")})
