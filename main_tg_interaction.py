from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    JobQueue,
)
from telegram.constants import ParseMode
import pytz
import re

from src.agent import FinanceAgent
from os import getenv

TOKEN = getenv("TG_TOKEN", "")
agent = FinanceAgent(model="gpt-3.5-turbo", verbose=False)


def escape_markdown_v2(text: str) -> str:
    """
    Escape special characters for Telegram MarkdownV2 format.

    Args:
        text: The text to escape

    Returns:
        Escaped text safe for MarkdownV2 parsing
    """
    # Characters that need to be escaped in MarkdownV2
    escape_chars = r"_*[]()~`>#+-=|{}.!"

    # Escape each character
    escaped_text = text
    for char in escape_chars:
        escaped_text = escaped_text.replace(char, f"\\{char}")

    return escaped_text


# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = "Hello! I am your finance bot 🤖"
    await update.message.reply_text(
        escape_markdown_v2(welcome_message), parse_mode=ParseMode.MARKDOWN_V2
    )


# message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        result = agent.execute_request(user_message)
        if result["success"]:
            response = result["output"]
        else:
            response = result["error"]

        # Escape the response for MarkdownV2
        escaped_response = escape_markdown_v2(response)
        await update.message.reply_text(
            escaped_response, parse_mode=ParseMode.MARKDOWN_V2
        )

    except KeyboardInterrupt:
        print("\n⚠️ Request interrupted.")
        error_msg = "Request was interrupted. Try again."
        await update.message.reply_text(
            escape_markdown_v2(error_msg), parse_mode=ParseMode.MARKDOWN_V2
        )
    except Exception as e:
        error_response = f"An error occurred: {str(e)}"
        await update.message.reply_text(
            escape_markdown_v2(error_response), parse_mode=ParseMode.MARKDOWN_V2
        )


def main():
    # Create application builder
    builder = ApplicationBuilder()
    builder.token(TOKEN)
    app = builder.build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
