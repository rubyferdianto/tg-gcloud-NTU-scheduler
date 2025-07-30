import os
import sys
import logging
import asyncio
from flask import Flask, request, jsonify

# Add the src directory to the Python path
sys.path.append('/app/src')

from telegram_bot import TelegramBot
from scheduler import schedule_daily_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the Telegram bot in webhook mode
telegram_bot = TelegramBot(webhook_mode=True)

# Set up the scheduler for daily notifications
schedule_daily_notification(telegram_bot)

@app.route('/')
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({"status": "healthy", "message": "Telegram bot is running"})

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
