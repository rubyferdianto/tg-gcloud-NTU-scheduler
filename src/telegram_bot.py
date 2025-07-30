import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os

logging.basicConfig(level=logging.INFO)

class TelegramBot:
    def __init__(self, webhook_mode=False):
        print("Initializing TelegramBot...")
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")
        
        self.webhook_mode = webhook_mode
        self.application = Application.builder().token(self.token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_menu_selection))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info("Received /start command")
        menu_keyboard = [
        ['QR-Code Module 1', 'QR-Code Module 2'],
        ['QR-Code Module 3', 'QR-Code Module 4'],
        ['QR-Code Module 5', 'QR-Code Module 6']]

        reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True, one_time_keyboard=False)
        await update.message.reply_text(
            "Welcome! Please choose an option:",
            reply_markup=reply_markup
        )

    async def handle_menu_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        url = "https://www.myskillsfuture.gov.sg/api/take-attendance/"

        # Send the new message and store its message_id
        if text == "QR-Code Module 1":
            sent = await update.message.reply_text(
                f"Tap to open: [Module 1 Attendance]({url}RA576069)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 2":
            sent = await update.message.reply_text(
                f"Tap to open: [Module 2 Attendance]({url}RA576073)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 3":
            sent = await update.message.reply_text(
                f"Tap to open: [Module 3 Attendance]({url}RA576079)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 4":
            sent = await update.message.reply_text(
                f"Tap to open: [Module 4 Attendance]({url}RA576096)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 5":
            sent = await update.message.reply_text(
                f"Tap to open: [Module 5 Attendance]({url}RA576098)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 6":
            sent = await update.message.reply_text(
                f"Tap to open: [Module 6 Attendance]({url}RA576102)",
                parse_mode='Markdown'
            )
        else:
            sent = await update.message.reply_text("Please select a valid option from the menu.")

        # Store the last bot message id
        context.user_data["last_bot_message_id"] = sent.message_id

    async def send_message(self, chat_id, text):
        await self.application.bot.send_message(chat_id=chat_id, text=text)

    def run(self):
        if self.webhook_mode:
            print("TelegramBot is configured for webhook mode - use with Flask app")
        else:
            print("Starting TelegramBot polling...")
            self.application.run_polling()
    
    async def set_webhook(self, webhook_url):
        """Set webhook for the bot"""
        await self.application.initialize()
        await self.application.bot.set_webhook(url=webhook_url)
        
    async def process_update(self, update_data):
        """Process incoming webhook update"""
        await self.application.initialize()
        update = Update.de_json(update_data, self.application.bot)
        await self.application.process_update(update)
