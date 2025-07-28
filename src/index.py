import huggingface_client
from telegram_bot import TelegramBot
from huggingface_client import HuggingFaceClient
from scheduler import schedule_daily_notification
import telegram_bot

def main():
    telegram_bot = TelegramBot()
    huggingface_client = HuggingFaceClient("bert-base-uncased")
    
    schedule_daily_notification(telegram_bot)
    telegram_bot.run()

if __name__ == "__main__":
    main()