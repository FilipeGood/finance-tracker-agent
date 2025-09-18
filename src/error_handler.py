"""
Error Handler Module

Shared error handling patterns and utilities for the Finance Tracker Agent.
Provides consistent error processing across different interfaces.
"""

from typing import Dict, Any, Tuple, Optional


class AgentErrorHandler:
    """
    Centralized error handling for agent responses and exceptions.

    Provides consistent error processing patterns that can be used
    across terminal and Telegram interfaces.
    """

    @staticmethod
    def process_agent_response(
        response: Dict[str, Any],
    ) -> Tuple[str, bool, Optional[str]]:
        """
        Process agent response and extract relevant information.

        Args:
            response: Agent response dictionary containing success status and output

        Returns:
            Tuple of (output_message, is_success, error_details)
        """
        success = response.get("success", False)

        if success:
            output = response.get("output", "Request completed successfully")
            return output, True, None
        else:
            # Handle error response
            output = response.get("output", "An error occurred")
            error = response.get("error")
            return output, False, error

    @staticmethod
    def format_error_details(error: Any, max_length: int = 200) -> str:
        """
        Format error details for display with length limit.

        Args:
            error: Error object or string to format
            max_length: Maximum length for error message

        Returns:
            Formatted error string
        """
        if not error:
            return ""

        error_str = str(error)
        if len(error_str) > max_length:
            return f"{error_str[:max_length]}..."
        return error_str

    @staticmethod
    def is_api_error(error: Any) -> bool:
        """
        Check if error is related to API issues.

        Args:
            error: Error to check

        Returns:
            True if error appears to be API-related
        """
        if not error:
            return False
        return "API" in str(error).upper()

    @staticmethod
    def handle_keyboard_interrupt() -> str:
        """
        Get standard message for keyboard interrupt.

        Returns:
            Standard interruption message
        """
        return "⚠️ Request was interrupted. Please try again."

    @staticmethod
    def handle_unexpected_error(error: Exception, max_length: int = 100) -> str:
        """
        Format unexpected error for user display.

        Args:
            error: Exception that occurred
            max_length: Maximum length for error details

        Returns:
            Formatted error message for users
        """
        error_details = AgentErrorHandler.format_error_details(error, max_length)
        return (
            f"❌ An unexpected error occurred while processing your request.\n\n"
            f"🔧 Error: {error_details}"
        )

    @staticmethod
    def should_show_technical_details(error: Any, verbose: bool = False) -> bool:
        """
        Determine if technical error details should be shown to user.

        Args:
            error: Error to evaluate
            verbose: Whether verbose mode is enabled

        Returns:
            True if technical details should be displayed
        """
        if not error:
            return False

        # Always show API errors as they're often actionable
        if AgentErrorHandler.is_api_error(error):
            return True

        # Show all errors in verbose mode
        return verbose
