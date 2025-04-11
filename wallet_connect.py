from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # pour autoriser les requêtes du frontend

@app.route('/')
def index():
    return 'Passworld backend is alive'

@app.route('/connect')
def connect_wallet():
    tg_id = request.args.get("tg_id")
    return render_template('wallet_connect.html', tg_id=tg_id)

@app.route('/verify', methods=['POST'])
def verify_signature():
    data = request.json
    # TODO : Ajouter la vérification de signature ici
    # Pour l'instant on simule une validation OK
    return jsonify({"status": "success", "wallet": data.get("address")})
