# Telegram Hugging Face Notifier

This project is a Telegram bot that sends daily notifications using predictions from a Hugging Face model. The bot is scheduled to run every day at 7 PM.

## Project Structure

```
src
├── index.py               # Entry point of the application
├── telegram_bot.py        # Implementation of the Telegram bot
├── huggingface_client.py   # Interaction with the Hugging Face API
└── scheduler.py           # Scheduling of daily notifications
requirements.txt           # Project dependencies
README.md                  # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/telegram-hf-notifier.git
   cd telegram-hf-notifier
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Telegram bot:
   - Create a new bot using [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
   - Obtain your bot token.

4. Configure the bot token in the `src/index.py` file.

5. (Optional) Configure the Hugging Face model you want to use in `src/huggingface_client.py`.

## Usage

To run the application, execute the following command:
```
python src/index.py
```

The bot will start and send notifications every day at 7 PM based on the predictions from the specified Hugging Face model.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.