import asyncio
import logging
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_daily_notification(telegram_bot):
    """Send daily notification to remind about check-in"""
    try:
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Send the message
        loop.run_until_complete(
            telegram_bot.send_message(7590222815, "🕖 It's 7 PM! Time to check-in for NTU classes! 📚")
        )
        
        # Close the loop
        loop.close()
        
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