import hashlib
import sqlite3
import os
import time
import uuid
from solana.rpc.api import Client
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# === CONFIG ===
BONKWORD_POT_ADDRESS = "BONK_WALLET_ADDRESS"
BONKWORD_PRIVATE_KEY = "path/to/pot-wallet.json"
INITIAL_BONK_PER_GUESS = 100000
BONK_INCREMENT = 1
HASH_SECRET = "super_secret_salt"
INDICE_DU_JOUR = "It's about Law"
WEB_CONNECT_URL = "https://yourdomain.com/connect"  # à remplacer par ton URL de connexion wallet

# === DATABASE SETUP ===
conn = sqlite3.connect("bonkword.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS game (
    date TEXT PRIMARY KEY,
    word TEXT,
    hash TEXT,
    winner TEXT
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS guesses (
    username TEXT,
    guess TEXT,
    date TEXT
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS wallets (
    username TEXT PRIMARY KEY,
    wallet TEXT,
    credits INTEGER DEFAULT 0
)
""")
conn.commit()

# === WORD UTILS ===
def hash_word(word: str) -> str:
    return hashlib.sha256((HASH_SECRET + word.lower()).encode()).hexdigest()

def store_daily_word(word: str):
    today = time.strftime("%Y-%m-%d")
    h = hash_word(word)
    c.execute("INSERT OR REPLACE INTO game (date, word, hash, winner) VALUES (?, ?, ?, ?)",
              (today, word, h, None))
    conn.commit()

def get_daily_hash():
    today = time.strftime("%Y-%m-%d")
    c.execute("SELECT hash FROM game WHERE date = ?", (today,))
    row = c.fetchone()
    return row[0] if row else None

def set_winner(username):
    today = time.strftime("%Y-%m-%d")
    c.execute("UPDATE game SET winner = ? WHERE date = ?", (username, today))
    conn.commit()

def get_guess_count():
    today = time.strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM guesses WHERE date = ?", (today,))
    return c.fetchone()[0]

def get_unique_users():
    today = time.strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(DISTINCT username) FROM guesses WHERE date = ?", (today,))
    return c.fetchone()[0]

def get_guess_price():
    return INITIAL_BONK_PER_GUESS + BONK_INCREMENT * get_guess_count()

def get_all_guesses():
    today = time.strftime("%Y-%m-%d")
    c.execute("SELECT DISTINCT guess FROM guesses WHERE date = ?", (today,))
    rows = c.fetchall()
    return [row[0] for row in rows]

def get_wallet(username):
    c.execute("SELECT wallet FROM wallets WHERE username = ?", (username,))
    row = c.fetchone()
    return row[0] if row else None

def get_credits(username):
    c.execute("SELECT credits FROM wallets WHERE username = ?", (username,))
    row = c.fetchone()
    return row[0] if row else 0

def deduct_credit(username):
    c.execute("UPDATE wallets SET credits = credits - 1 WHERE username = ?", (username,))
    conn.commit()

# === TELEGRAM BOT ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.username or update.message.from_user.first_name
    session_id = str(uuid.uuid4())
    connect_link = f"{WEB_CONNECT_URL}?session={session_id}&user={user}"
    price = get_guess_price()
    attempts = get_guess_count()
    players = get_unique_users()

    welcome_msg = (
        f"🐶 Welcome to *PASSWORLD* — web3 game powered by BONK on Telegram !\n"
        "A secret word is hidden every day. Guess it to win the pot !\n"
        "Each guess costs *100K BONK* at the beginning. The price increases x2 every 50 guesses tried.\n\n"
        "🎮 *How to play :*\n"
        "1. Connect your wallet\n"
        "2. Use `/guess ` to try a word\n"
        "3. You can also buy *guess packs* at lowest price per guess\n\n"
        f"💰 *Estimated pot* : {price * attempts} BONK\n"
        f"🔥 *Guess price* : {price} BONK\n"
        f"👥 *Players today* : {players}\n"
        f"🧩 *Hint* : {INDICE_DU_JOUR}\n\n"
        f"🔐 *Connect your wallet ici* : [Se connecter]({connect_link})\n"
        "📦 Type `/buy 10` to get a pack of 10 guesses to get -10%/guess."
    )

    keyboard = [
        [InlineKeyboardButton("🔗 Connect my Wallet", url=connect_link)],
        [InlineKeyboardButton("💡 View hint", callback_data="show_hint")],
        [InlineKeyboardButton("📜 Tried words", callback_data="show_guesses")],
        [InlineKeyboardButton("📊 Today's stats", callback_data="show_stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_msg, parse_mode="Markdown", reply_markup=reply_markup, disable_web_page_preview=True)

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /guess word")
        return
    word = context.args[0].lower()
    user = update.message.from_user.username or update.message.from_user.first_name

    if get_credits(user) <= 0:
        await update.message.reply_text("❌ You have no more credits. Buy a pack with `/buy 10`.")
        return

    hashed_guess = hash_word(word)
    correct_hash = get_daily_hash()
    if not correct_hash:
        await update.message.reply_text("No active word today. Come back later.")
        return

    today = time.strftime("%Y-%m-%d")
    c.execute("INSERT INTO guesses (username, guess, date) VALUES (?, ?, ?)", (user, word, today))
    deduct_credit(user)
    conn.commit()

    if hashed_guess == correct_hash:
        set_winner(user)
        await update.message.reply_text(f"🔥 CONGRATS @{user} ! You found the word and won the pot !")
    else:
        await update.message.reply_text("🐶 Nope! Try again.")

async def guesses_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guesses = get_all_guesses()
    if not guesses:
        await update.message.reply_text("No guesses today.")
        return
    msg = "📜 Tried words aujourd'hui:\n" + ", ".join(guesses)
    await update.message.reply_text(msg)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_hint":
        await query.edit_message_text(f"🧩 Hints : {INDICE_DU_JOUR}")
    elif query.data == "show_guesses":
        guesses = get_all_guesses()
        msg = "📜 Tried words aujourd'hui:\n" + ", ".join(guesses) if guesses else "No guesses today."
        await query.edit_message_text(msg)
    elif query.data == "show_stats":
        price = get_guess_price()
        attempts = get_guess_count()
        players = get_unique_users()
        msg = (
            f"📊 Today's stats :\n"
            f"• Estimated pot : {price * attempts} BONK\n"
            f"• Guess price : {price} BONK\n"
            f"• Number of attempts : {attempts}\n"
            f"• Players : {players}"
        )
        await query.edit_message_text(msg)

# === WALLET & SOLANA ===
client = Client("https://api.mainnet-beta.solana.com")

# === MAIN APP ===
app = ApplicationBuilder().token("7900736485:AAH3a6mW89OSbpl3LkPZZaGjkvAEJueTnW0").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("guess", guess))
app.add_handler(CommandHandler("guesses", guesses_list))
app.add_handler(CallbackQueryHandler(handle_buttons))

if __name__ == '__main__':
    print("Launching BONKWORD bot...")
    app.run_polling()

# === Render-compatible Flask app ===
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"
