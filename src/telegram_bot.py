import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)

class TelegramBot:
    def __init__(self):
        print("Initializing TelegramBot...")
        self.token = "8300049409:AAGhYomw0vvPDwabom3jbj7pq2oSVjRNqoE"
        self.updater = Updater(self.token, use_context=True)
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_menu_selection))

    def start(self, update: Update, context: CallbackContext):
        logging.info("Received /start command")
        menu_keyboard = [
        ['QR-Code Module 1', 'QR-Code Module 2'],
        ['QR-Code Module 3', 'QR-Code Module 4'],
        ['QR-Code Module 5', 'QR-Code Module 6']]

        reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True, one_time_keyboard=False)
        update.message.reply_text(
            "Welcome! Please choose an option:",
            reply_markup=reply_markup
        )

    def handle_menu_selection(self, update: Update, context: CallbackContext):
        text = update.message.text
        url = "https://www.myskillsfuture.gov.sg/api/take-attendance/"

        # Send the new message and store its message_id
        if text == "QR-Code Module 1":
            sent = update.message.reply_text(
                f"Tap to open: [Module 1 Attendance]({url}RA576069)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 2":
            sent = update.message.reply_text(
                f"Tap to open: [Module 2 Attendance]({url}RA576073)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 3":
            sent = update.message.reply_text(
                f"Tap to open: [Module 3 Attendance]({url}RA576079)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 4":
            sent = update.message.reply_text(
                f"Tap to open: [Module 4 Attendance]({url}RA576096)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 5":
            sent = update.message.reply_text(
                f"Tap to open: [Module 5 Attendance]({url}RA576098)",
                parse_mode='Markdown'
            )
        elif text == "QR-Code Module 6":
            sent = update.message.reply_text(
                f"Tap to open: [Module 6 Attendance]({url}RA576102)",
                parse_mode='Markdown'
            )
        else:
            sent = update.message.reply_text("Please select a valid option from the menu.")

        # Store the last bot message id
        context.user_data["last_bot_message_id"] = sent.message_id

    def send_message(self, chat_id, text):
        self.updater.bot.send_message(chat_id=chat_id, text=text)

    def run(self):
        print("Starting TelegramBot polling...")
        self.updater.start_polling()
        self.updater.idle()
