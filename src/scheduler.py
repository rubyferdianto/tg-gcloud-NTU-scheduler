from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from telegram_bot import TelegramBot

def send_daily_notification(telegram_bot):
    #print('START inside calling send_daily_notification')
    telegram_bot.send_message(7590222815, "Its 7 PM! Time to check-in NTU")
    #print('END inside calling send_daily_notification')

def schedule_daily_notification(telegram_bot):
    sg_timezone = pytz.timezone("Asia/Singapore")
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_notification, 'cron', 
                      args=[telegram_bot],
                      hour=19, minute=00, 
                      timezone=sg_timezone)
    scheduler.start()