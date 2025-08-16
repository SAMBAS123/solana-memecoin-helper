import os
from telegram import Bot

def send_alert(message):
    """Sends an alert via Telegram bot, configurable via env."""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        try:
            bot = Bot(token=token)
            bot.send_message(chat_id=chat_id, text=f"ALERT: {message}")
        except Exception as e:
            print(f"Telegram alert failed: {str(e)}")
    else:
        print(f"ALERT: {message} (Telegram not configured)")
