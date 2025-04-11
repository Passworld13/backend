
import logging
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# === FLASK SETUP ===
app = Flask(__name__)

@app.route("/")
def home():
    return "Server is up ✅"

# === TELEGRAM BOT SETUP ===
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace this with your real token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello from the bot 👋")

def setup_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    return application

# === MAIN LOGIC ===
def run():
    loop = asyncio.get_event_loop()
    bot_app = setup_bot()
    loop.create_task(bot_app.run_polling())
    app.run(host="0.0.0.0", port=10000)

# === GUNICORN ENTRYPOINT ===
if __name__ != "__main__":
    bot_app = setup_bot()
    asyncio.get_event_loop().create_task(bot_app.run_polling())

# === DEV ENTRYPOINT ===
if __name__ == "__main__":
    run()
