"""
Terminal Interface Module

This module contains the TerminalInterface class that handles user interaction
for the personal finance tracker through a command-line interface.
"""

import sys
from typing import Dict, Any, Optional


class TerminalInterface:
    """
    Terminal interface for the Finance Agent.

    Provides a clean command-line interface for users to interact with the
    finance tracking agent through natural language input and formatted output.
    """

    def __init__(self, use_colors: bool = True):
        """
        Initialize the terminal interface.

        Args:
            use_colors: Whether to use ANSI color codes for enhanced output formatting
        """
        self.use_colors = use_colors and self._supports_color()
        self.exit_commands = {"quit", "exit", "q", "bye", "goodbye"}
        self.help_commands = {"help", "h", "?", "commands"}

    def _supports_color(self) -> bool:
        """Check if terminal supports ANSI color codes."""
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    def _colorize(self, text: str, color_code: str) -> str:
        """Apply ANSI color codes to text if colors are enabled."""
        if not self.use_colors:
            return text
        return f"\033[{color_code}m{text}\033[0m"

    def _green(self, text: str) -> str:
        """Apply green color to text."""
        return self._colorize(text, "32")

    def _red(self, text: str) -> str:
        """Apply red color to text."""
        return self._colorize(text, "31")

    def _blue(self, text: str) -> str:
        """Apply blue color to text."""
        return self._colorize(text, "34")

    def _yellow(self, text: str) -> str:
        """Apply yellow color to text."""
        return self._colorize(text, "33")

    def _bold(self, text: str) -> str:
        """Apply bold formatting to text."""
        return self._colorize(text, "1")

    def display_welcome(self) -> None:
        """
        Display welcome message with usage instructions.

        Shows the application header, available functionality, and example commands
        to help users get started with the finance tracker.
        """
        welcome_text = f"""
            {self._bold(self._blue("=" * 60))}
            {self._bold(self._blue("           Personal Finance Tracker Agent"))}
            {self._bold(self._blue("=" * 60))}

            {self._green("Welcome!")} I'm your personal finance assistant. I can help you:

            {self._yellow("📊 Track Expenses:")}
            • Add new expenses with natural language
            • Update or correct recent expenses
            • Categorize spending automatically

            {self._yellow("📈 Generate Reports:")}
            • View spending by category, time period, or account
            • Analyze spending patterns and trends
            • Get financial insights and summaries

            {self._yellow("💡 Example Commands:")}
            • "Add new expense in a restaurant 56 euros today"
            • "I bought groceries for 45 euros yesterday"
            • "Give me my spendings for the last week"
            • "Show spending by category for this month"
            • "Update the last expense to be Entertainment/Movies"

            {self._yellow("🔧 Available Commands:")}
            • {self._green("help")} or {self._green("?")} - Show this help message
            • {self._green("quit")} or {self._green("exit")} - Exit the application

            {self._blue("Type your request in natural language and press Enter to begin!")}
            {self._bold(self._blue("-" * 60))}
        """
        print(welcome_text)

    def display_help(self) -> None:
        """
        Display help information for available commands and functionality.
        """
        help_text = f"""
            {self._bold(self._yellow("Finance Tracker Help"))}
            {self._yellow("=" * 25)}

            {self._green("Expense Management:")}
            • Add expenses: "Save a $15 coffee expense"
            • Update categories: "Change the last expense to Food/Restaurant"
            • Add notes: "Record dinner for $25 with friends"

            {self._green("Reporting & Analysis:")}
            • Monthly reports: "Show my spending for January 2025"
            • Category breakdowns: "Get spending by category this month"
            • Account summaries: "Show spending from my Food Account"
            • Time-based analysis: "Analyze my spending patterns"

            {self._green("Categories Available:")}
            • Food, Transportation, Entertainment, Health, Shopping, 
                Bills, Education, Travel, Personal Care, Other

            {self._green("Accounts:")}
            • Main Account (default), Food Account, or specify your own

            {self._green("Commands:")}
            • {self._yellow("help")} - Show this help
            • {self._yellow("quit")} or {self._yellow("exit")} - Exit application

            {self._blue("💡 Tip: Use natural language! The agent understands context and can infer missing details.")}
            """
        print(help_text)

    def get_user_input(self) -> Optional[str]:
        """
        Capture user input from the terminal.

        Returns:
            User input string, or None if an exit command was entered

        Handles:
            - Exit commands (quit, exit, etc.)
            - Help commands
            - Empty input validation
            - Keyboard interrupts (Ctrl+C)
        """
        try:
            while True:
                # Display prompt
                user_input = input(
                    f"\n{self._green('💬')} {self._bold('You:')} "
                ).strip()

                # Handle empty input
                if not user_input:
                    print(
                        f"{self._yellow('⚠️')} Please enter a command or type 'help' for assistance."
                    )
                    continue

                # Check for exit commands
                if user_input.lower() in self.exit_commands:
                    return None

                # Check for help commands
                if user_input.lower() in self.help_commands:
                    self.display_help()
                    continue

                return user_input

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print(
                f"\n\n{self._yellow('👋')} Goodbye! Thanks for using the Finance Tracker."
            )
            return None
        except EOFError:
            # Handle Ctrl+D gracefully
            print(
                f"\n\n{self._yellow('👋')} Goodbye! Thanks for using the Finance Tracker."
            )
            return None

    def display_response(self, response: Dict[str, Any]) -> None:
        """
        Format and display the agent's response.

        Args:
            response: Dictionary containing the agent's response with keys:
                     - success: Boolean indicating execution success
                     - output: Agent's response message
                     - error: Error details if execution failed

        Formats the response with appropriate colors and icons based on success status.
        """
        print(f"\n{self._blue('🤖')} {self._bold('Finance Agent:')}")

        if response.get("success", False):
            # Successful response
            output = response.get("output", "No response received")
            print(f"{self._green('✅')} {output}")
        else:
            # Error response
            output = response.get("output", "An error occurred")
            error = response.get("error")

            print(f"{self._red('❌')} {output}")

            # Show detailed error in verbose mode or if it's a critical error
            if error and "API" in str(error):
                print(f"{self._red('🔧')} {self._yellow('Technical details:')} {error}")

    def display_goodbye(self) -> None:
        """
        Display goodbye message when user exits the application.
        """
        goodbye_text = f"""
            {self._green("👋")} Thank you for using the Personal Finance Tracker!

            {self._blue("💡")} Your financial data has been saved and is ready for your next session.
            {self._blue("📊")} Keep tracking your expenses to build better financial habits!

            {self._yellow("Have a great day! 🌟")}
            """
        print(goodbye_text)

    def display_error(self, error_message: str) -> None:
        """
        Display a formatted error message.

        Args:
            error_message: The error message to display
        """
        print(f"\n{self._red('❌ Error:')} {error_message}")

    def display_info(self, info_message: str) -> None:
        """
        Display a formatted informational message.

        Args:
            info_message: The informational message to display
        """
        print(f"\n{self._blue('ℹ️')} {info_message}")
