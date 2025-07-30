from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_daily_notification(telegram_bot):
    """Send daily notification to remind about check-in"""
    try:
        # Use asyncio to run the async send_message method
        asyncio.run(telegram_bot.send_message(7590222815, "Its 7 PM! Time to check-in NTU"))
        logger.info("Daily notification sent successfully")
    except Exception as e:
        logger.error(f"Failed to send daily notification: {e}")

def schedule_daily_notification(telegram_bot):
    """Schedule daily notifications at 7 PM Singapore time"""
    sg_timezone = pytz.timezone("Asia/Singapore")
    scheduler = BackgroundScheduler(timezone=sg_timezone)
    
    scheduler.add_job(
        send_daily_notification, 
        'cron',
        args=[telegram_bot],
        hour=19, 
        minute=0,
        id='daily_notification',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started - daily notifications set for 7:00 PM Singapore time")
    
    return scheduler