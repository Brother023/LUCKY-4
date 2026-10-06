import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Setup basic logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# A simple dictionary acting as a database for demo purposes
# In a real bot, you might scrape this or use an API.
ERROR_DB = {
    "404": "Not Found. The requested resource could not be found on the server.",
    "500": "Internal Server Error. The server encountered an unexpected condition.",
    "403": "Forbidden. The server understood the request but refuses to authorize it.",
    "timeout": "The connection timed out. Check your internet connection or server status."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message when the command /start is issued."""
    user = update.effective_user
    # Generic, non-promotional greeting
    await update.message.reply_text(
        f"Hello {user.first_name}. I am an error code lookup utility.\n\n"
        "Send me an error code (e.g., 404) or use /help to see commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message when the command /help is issued."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Restart the bot\n"
        "/help - Show this message\n\n"
        "You can also simply type an error code like '404' or '500' to get a definition."
    )

async def lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /lookup command if user wants to search specifically."""
    if not context.args:
        await update.message.reply_text("Please provide an error code. Example: /lookup 404")
        return
    code = context.args[0].lower()
    await send_error_info(update, code)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles plain text messages (error codes)."""
    text = update.message.text.lower().strip()
    # Basic check to avoid spamming on random long messages
    if len(text) < 20:
        await send_error_info(update, text)
    else:
        await update.message.reply_text("Please enter a short error code (e.g., '404') or use /help.")

async def send_error_info(update: Update, code: str):
    """Utility function to lookup and reply."""
    info = ERROR_DB.get(code)
    if info:
        await update.message.reply_text(f"Error Code: {code.upper()}\n\nDetails: {info}")
    else:
        await update.message.reply_text(
            f"Sorry, I do not have specific information for '{code}'. "
            "Please ensure the code is correct or try a common HTTP status code."
        )

def main():
    """Start the bot."""
    # Railway will inject the TOKEN environment variable if you set it in the dashboard
    # Or replace the string below with your token directly.
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_API_TOKEN_HERE")
    
    if token == "YOUR_API_TOKEN_HERE":
        print("ERROR: Please set your TELEGRAM_BOT_TOKEN environment variable.")
        return

    application = ApplicationBuilder().token(token).build()

    # Command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('lookup', lookup))
    
    # Message handler for plain text (error codes)
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
