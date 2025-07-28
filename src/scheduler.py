from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from telegram_bot import TelegramBot
from huggingface_client import HuggingFaceClient

def send_daily_notification():
    hf_client = HuggingFaceClient()
    prediction = hf_client.get_model_prediction()
    
    bot = TelegramBot()
    bot.send_message(prediction)

def schedule_daily_notification():
    scheduler = BlockingScheduler()
    scheduler.add_job(send_daily_notification, 'cron', hour=19, minute=0)
    scheduler.start()