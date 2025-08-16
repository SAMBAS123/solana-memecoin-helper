import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

async def send_test():
    bot = Bot(os.getenv('TELEGRAM_TOKEN'))
    await bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text='Async test from Grok: Bot is online! Send /start or /quickscan <token> in Telegram.')

if __name__ == '__main__':
    asyncio.run(send_test())
