from flask import Flask
from admin_route import admin_bp
from guess_route import guess_bp
app.register_blueprint(guess_bp)

app = Flask(__name__)
app.register_blueprint(admin_bp)

@app.route("/")
def index():
    return "Bienvenue sur l'API Passworld 🧠🔐"

if __name__ == "__main__":
    app.run(debug=True)

