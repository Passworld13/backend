
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running properly!'

# ---- Telegram bot logic goes here ----
# This section should be protected to only run when needed, not on module import

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
