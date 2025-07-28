import huggingface_client
from telegram_bot import TelegramBot
from huggingface_client import HuggingFaceClient
from scheduler import schedule_daily_notification

def main():
    telegram_bot = TelegramBot()
    huggingface_client = HuggingFaceClient("bert-base-uncased")  # <-- Add a model name

    result = huggingface_client.predict("The capital of France is [MASK].")
    print(result)

    # Schedule the daily notification at 7 PM
    schedule_daily_notification(telegram_bot, huggingface_client)

    telegram_bot.run()

if __name__ == "__main__":
    main()