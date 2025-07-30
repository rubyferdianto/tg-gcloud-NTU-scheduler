import os
import sys
import logging
import asyncio
from flask import Flask, request, jsonify

from telegram_bot import TelegramBot
from scheduler import schedule_daily_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the Telegram bot based on mode
webhook_mode = os.getenv('WEBHOOK_MODE', 'true').lower() == 'true'
telegram_bot = TelegramBot(webhook_mode=webhook_mode)

# Set up the scheduler for daily notifications
scheduler = schedule_daily_notification(telegram_bot)

def run_polling_mode():
    """Run bot in polling mode for local development"""
    print("Starting Telegram Bot in polling mode for local development...")
    logger.info("Bot running in polling mode")
    telegram_bot.run()

def run_webhook_mode():
    """Run bot in webhook mode for production"""
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Bot running in webhook mode on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

@app.route('/')
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        "status": "healthy", 
        "message": "Telegram bot is running",
        "scheduler_running": scheduler.running if scheduler else False,
        "next_notification": "7:00 PM Singapore time daily"
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint to keep container warm"""
    return jsonify({"status": "pong", "timestamp": "now"})

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates from Telegram"""
    try:
        update_data = request.get_json()
        if update_data:
            # Run the async process_update in a new event loop
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(telegram_bot.process_update(update_data))
                loop.close()
            except Exception as e:
                logger.error(f"Error in async processing: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500
             
            return jsonify({"status": "ok"})
        else:
            logger.warning("Received empty update")
            return jsonify({"status": "error", "message": "Empty update"}), 400
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['POST'])
def set_webhook():
    """Set the webhook URL for the bot"""
    try:
        webhook_url = os.getenv("WEBHOOK_URL")
        if not webhook_url:
            return jsonify({"status": "error", "message": "WEBHOOK_URL not set"}), 400
        
        full_webhook_url = f"{webhook_url}/webhook"
        
        # Run the async set_webhook in a new event loop
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(telegram_bot.set_webhook(full_webhook_url))
            loop.close()
        except Exception as e:
            logger.error(f"Error setting webhook: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
        
        logger.info(f"Webhook set to: {full_webhook_url}")
        return jsonify({"status": "ok", "webhook_url": full_webhook_url})
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/trigger_notification', methods=['POST'])
def trigger_notification():
    """Manually trigger a notification for testing"""
    try:
        # Run the async process_update in a new event loop
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                telegram_bot.send_message(7590222815, "🧪 Test notification: Time to check-in for NTU classes! 📚")
            )
            loop.close()
        except Exception as e:
            logger.error(f"Error in manual notification: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
        
        return jsonify({"status": "ok", "message": "Test notification sent"})
    except Exception as e:
        logger.error(f"Error triggering notification: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Check if we should run in polling mode (for local development)
    if len(sys.argv) > 1 and sys.argv[1] == '--polling':
        run_polling_mode()
    elif not webhook_mode:
        run_polling_mode() 
    else:
        run_webhook_mode()
