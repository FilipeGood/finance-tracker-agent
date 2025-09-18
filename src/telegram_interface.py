"""
Telegram Interface Module

This module contains the TelegramInterface class that handles user interaction
for the personal finance tracker through a Telegram bot interface. Part of the
unified application architecture, this interface provides seamless Telegram
integration with shared error handling and configuration management.

Features:
    - Full Telegram Bot API integration
    - MarkdownV2 message formatting with proper escaping
    - Shared error handling and message formatting
    - Production-ready bot lifecycle management
    - Graceful shutdown handling
"""

import sys
from typing import TYPE_CHECKING

from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ParseMode

from .config import AppConfig, ConfigurationError
from .error_handler import AgentErrorHandler
from .feedback import MessageFormatter, WelcomeMessages

if TYPE_CHECKING:
    from .agent import FinanceAgent


class TelegramInterface:
    """
    Telegram bot interface for the Finance Agent in the unified application architecture.

    Provides a Telegram bot interface for users to interact with the finance tracking
    agent through natural language messages. Integrates with the shared configuration
    management and error handling patterns established in the unified main entry point.

    Features:
        - Complete Telegram Bot API integration with proper message handling
        - MarkdownV2 formatting with comprehensive character escaping
        - Shared error handling and response processing
        - Production-ready bot lifecycle and shutdown management
        - Integration with unified configuration validation
    """

    def __init__(self):
        """Initialize the Telegram interface."""
        self.agent = None

    def escape_markdown_v2(self, text: str) -> str:
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

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command for Telegram bot."""
        # Use shared welcome message
        welcome_message = WelcomeMessages.TELEGRAM_WELCOME

        await update.message.reply_text(
            self.escape_markdown_v2(welcome_message), parse_mode=ParseMode.MARKDOWN_V2
        )

    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages for Telegram bot."""
        user_message = update.message.text

        try:
            # Process request through agent
            result = self.agent.execute_request(user_message)

            # Use shared error handler to process response
            output, is_success, error = AgentErrorHandler.process_agent_response(result)

            # Format response based on success status
            if is_success:
                response = MessageFormatter.success_message(output)
            else:
                # Check if technical details should be shown
                if AgentErrorHandler.should_show_technical_details(error):
                    technical_details = AgentErrorHandler.format_error_details(
                        error, 200
                    )
                    response = MessageFormatter.error_message(output, technical_details)
                else:
                    response = MessageFormatter.error_message(output)

            # Escape the response for MarkdownV2 and send
            escaped_response = self.escape_markdown_v2(response)
            await update.message.reply_text(
                escaped_response, parse_mode=ParseMode.MARKDOWN_V2
            )

        except KeyboardInterrupt:
            print("\n⚠️ Request interrupted.")
            error_msg = AgentErrorHandler.handle_keyboard_interrupt()
            await update.message.reply_text(
                self.escape_markdown_v2(error_msg), parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as e:
            # Handle unexpected errors during agent processing
            error_response = AgentErrorHandler.handle_unexpected_error(e, 100)
            await update.message.reply_text(
                self.escape_markdown_v2(error_response),
                parse_mode=ParseMode.MARKDOWN_V2,
            )

    def run(self, agent: "FinanceAgent") -> None:
        """
        Start and run the Telegram bot interface.

        Args:
            agent: The FinanceAgent instance to use for processing requests

        Sets up and runs the Telegram bot, handling all message processing
        and bot lifecycle management.
        """
        self.agent = agent

        # Validate Telegram token using shared configuration
        try:
            token = AppConfig.get_telegram_token()
        except ConfigurationError as e:
            print(str(e))
            sys.exit(1)

        # Create application builder
        try:
            builder = ApplicationBuilder()
            builder.token(token)
            app = builder.build()
        except Exception as e:
            error_msg = MessageFormatter.error_message(
                f"Failed to create Telegram bot application: {e}"
            )
            print(error_msg)
            print(
                MessageFormatter.info_message(
                    "Please check your TG_TOKEN and try again."
                )
            )
            sys.exit(1)

        # Add handlers
        app.add_handler(CommandHandler("start", self.start_handler))
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler)
        )

        # Start bot
        print("🤖 Telegram bot is running...")
        print(
            MessageFormatter.info_message(
                "Send messages to your bot to interact with the Finance Agent"
            )
        )
        print("🔄 Press Ctrl+C to stop the bot")

        try:
            app.run_polling()
        except KeyboardInterrupt:
            print(f"\n\n👋 Telegram bot stopped. Thanks for using the Finance Tracker.")
        except Exception as e:
            error_msg = MessageFormatter.error_message(f"Telegram bot error: {e}")
            print(error_msg)
            print(
                MessageFormatter.info_message(
                    "Please check your configuration and try again."
                )
            )
            sys.exit(1)
