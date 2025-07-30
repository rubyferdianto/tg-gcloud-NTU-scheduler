from telegram_bot import TelegramBot
from scheduler import schedule_daily_notification

def main():
    """Main function for local development (polling mode)"""
    print("Starting Telegram Bot in polling mode for local development...")
    
    # Initialize the bot in polling mode
    telegram_bot = TelegramBot(webhook_mode=False)
    
    # Set up the scheduler for daily notifications
    schedule_daily_notification(telegram_bot)
    
    # Start the bot
    telegram_bot.run()

if __name__ == "__main__":
    main()