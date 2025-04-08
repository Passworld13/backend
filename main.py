from flask import Flask
from wallet_route import wallet_bp
from guess_route import guess_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(wallet_bp, url_prefix="/")
app.register_blueprint(guess_bp, url_prefix="/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
