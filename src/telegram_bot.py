from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

class TelegramBot:
    def __init__(self):
        self.token = "8300049409:AAGhYomw0vvPDwabom3jbj7pq2oSVjRNqoE"
        self.updater = Updater(self.token, use_context=True)
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_menu_selection))

    def start(self, update: Update, context: CallbackContext):
        menu_keyboard = [['QR-Code Module 1', 'QR-Code Module 2'], ['Help']]
        reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
        update.message.reply_text(
            "Welcome! Please choose an option:",
            reply_markup=reply_markup
        )

    def handle_menu_selection(self, update: Update, context: CallbackContext):
        text = update.message.text
        url = "https://www.myskillsfuture.gov.sg/api/take-attendance/"
        if text == "QR-Code Module 1":
            update.message.reply_text(url+"RA576069")
        elif text == "QR-Code Module 2":
            update.message.reply_text(url+"RA576073")
        elif text == "QR-Code Module 3":
            update.message.reply_text(url+"RA576079")
        elif text == "QR-Code Module 4":
            update.message.reply_text(url+"RA576096")
        elif text == "QR-Code Module 5":
            update.message.reply_text(url+"RA576098")
        elif text == "QR-Code Module 6":
            update.message.reply_text(url+"RA576102")        
        else:
            update.message.reply_text("Please select a valid option from the menu.")

    def run(self):
        self.updater.start_polling()
        self.updater.idle()