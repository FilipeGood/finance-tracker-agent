"""
Feedback Module

Consistent user feedback and messaging utilities for the Finance Tracker Agent.
Provides standardized message formatting across different interfaces.
"""

from typing import Optional


class MessageFormatter:
    """
    Standardized message formatting for user feedback.

    Provides consistent emoji usage, message structure, and
    formatting patterns across terminal and Telegram interfaces.
    """

    # Standard emoji patterns
    SUCCESS_EMOJI = "✅"
    ERROR_EMOJI = "❌"
    WARNING_EMOJI = "⚠️"
    INFO_EMOJI = "💡"
    TECHNICAL_EMOJI = "🔧"

    @staticmethod
    def success_message(message: str) -> str:
        """
        Format a success message.

        Args:
            message: Success message content

        Returns:
            Formatted success message
        """
        return f"{MessageFormatter.SUCCESS_EMOJI} {message}"

    @staticmethod
    def error_message(message: str, technical_details: Optional[str] = None) -> str:
        """
        Format an error message with optional technical details.

        Args:
            message: Main error message
            technical_details: Optional technical error details

        Returns:
            Formatted error message
        """
        formatted = f"{MessageFormatter.ERROR_EMOJI} {message}"

        if technical_details:
            formatted += f"\n\n{MessageFormatter.TECHNICAL_EMOJI} Technical details: {technical_details}"

        return formatted

    @staticmethod
    def warning_message(message: str) -> str:
        """
        Format a warning message.

        Args:
            message: Warning message content

        Returns:
            Formatted warning message
        """
        return f"{MessageFormatter.WARNING_EMOJI} {message}"

    @staticmethod
    def info_message(message: str) -> str:
        """
        Format an informational message.

        Args:
            message: Info message content

        Returns:
            Formatted info message
        """
        return f"{MessageFormatter.INFO_EMOJI} {message}"

    @staticmethod
    def configuration_error_message(error_msg: str, suggestion: str) -> str:
        """
        Format a configuration error with helpful suggestion.

        Args:
            error_msg: Configuration error message
            suggestion: Helpful suggestion for user

        Returns:
            Formatted configuration error message
        """
        return f"{MessageFormatter.error_message(error_msg)}\n{MessageFormatter.info_message(suggestion)}"


class WelcomeMessages:
    """Standard welcome and help messages for different interfaces."""

    TERMINAL_WELCOME = """
🚀 Welcome to your Personal Finance Tracker Agent!

Type your financial questions or commands in natural language:
• "Add expense of $50 for groceries today"
• "Show my spending this month" 
• "How much did I spend on dining last week?"

Commands:
• Type 'help' or '?' for assistance
• Type 'quit', 'exit', or 'q' to exit
• Use Ctrl+C to interrupt long operations

Let's get started with tracking your finances! 💰
"""

    TERMINAL_HELP = """
📖 Finance Tracker Help

Available Commands:
• help, h, ? - Show this help message
• quit, exit, q, bye, goodbye - Exit the application

Natural Language Examples:
• "Add $25 expense for lunch today"
• "Record a $200 grocery expense yesterday"
• "Show my total spending this month"
• "What did I spend on restaurants last week?"
• "Generate a spending report for August"
• "How much have I spent on utilities?"

Tips:
• Be specific with amounts, categories, and dates
• The agent understands various date formats
• You can ask for spending analysis and reports
• All data is stored locally in CSV format

Need more help? Just ask the agent directly! 🤖
"""

    TELEGRAM_WELCOME = """
🚀 *Welcome to your Personal Finance Tracker Agent\\!*

Send me your financial questions or commands in natural language:
• "Add expense of $50 for groceries today"
• "Show my spending this month" 
• "How much did I spend on dining last week?"

I understand natural language and can help you:
• Track expenses and income
• Generate spending reports
• Analyze your financial patterns
• Answer questions about your finances

Let's get started with tracking your finances\\! 💰
"""
