from flask import Flask, request

app = Flask(__name__)

@app.route("/api/connect-wallet", methods=["POST"])
def connect_wallet():
    data = request.get_json()
    wallet = data.get("wallet")
    telegram_id = data.get("telegram_id")
    print(f"[+] Wallet connecté: {wallet} pour Telegram ID: {telegram_id}")
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
