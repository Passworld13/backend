from flask import Flask
from admin_route import admin_bp

app = Flask(__name__)

app.register_blueprint(admin_bp)

if __name__ == "__main__":
   print("API Backend démarrée")
   app.run(debug=True)

