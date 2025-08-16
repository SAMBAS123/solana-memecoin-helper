import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from scanner import quick_scan  # Reuse existing scan

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def start(update, context):
    logging.debug("Received /start command")
    update.message.reply_text("Hi! Use /quickscan <token> to scan a memecoin.")

def quickscan(update, context):
    logging.debug("Received /quickscan command")
    if not context.args:
        update.message.reply_text("Please provide a token address, e.g., /quickscan DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263")
        return
    token = context.args[0]
    result = quick_scan(token)
    # Format result as text (or JSON if preferred)
    text = f"Scan for {token}:\nGMGN: {result['gmgn']}\nHolders: {result['holders']}\nLiq Alpha: {result['liq_alpha']}"
    update.message.reply_text(text)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("TELEGRAM_TOKEN not set in .env")
    else:
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("quickscan", quickscan))
        logging.debug("Starting bot polling")
        app.run_polling()
