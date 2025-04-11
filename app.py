from flask import Flask
from admin_route import admin_bp
from guess_route import guess_bp
from link_route import link_bp

app = Flask(__name__) 

app.register_blueprint(admin_bp)
app.register_blueprint(guess_bp)
app.register_blueprint(link_bp)

@app.route("/")
def index():
    return "Welcome to the Passworld API 🧠🔐"

if __name__ == "__main__":
    app.run(debug=True)


from flask import request

@app.route("/api/connect-wallet", methods=["POST"])
def connect_wallet():
    data = request.get_json()
    wallet = data.get("wallet")
    telegram_id = data.get("telegram_id")
    print(f"[+] Wallet connecté: {wallet} pour Telegram ID: {telegram_id}")
    return {"status": "ok"}, 200
