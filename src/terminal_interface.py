"""
Terminal Interface Module

This module contains the TerminalInterface class that handles user interaction
for the personal finance tracker through a command-line interface. Part of the
unified application architecture, this interface provides rich terminal output
with color support, graceful error handling, and comprehensive user guidance.

Features:
    - Rich terminal UI with ANSI color support
    - Comprehensive help and command guidance
    - Graceful keyboard interrupt handling
    - Shared error handling with other interfaces
    - Production-ready signal handling
"""

import sys
from typing import Dict, Any, Optional, TYPE_CHECKING

from .error_handler import AgentErrorHandler
from .feedback import MessageFormatter, WelcomeMessages

if TYPE_CHECKING:
    from .agent import FinanceAgent


class TerminalInterface:
    """
    Terminal interface for the Finance Agent in the unified application architecture.

    Provides a rich command-line interface for users to interact with the
    finance tracking agent through natural language input and formatted output.
    Integrates with the shared agent initialization and error handling patterns
    established in the unified main entry point.

    Features:
        - ANSI color support with fallback for non-color terminals
        - Comprehensive help system and command guidance
        - Graceful handling of user interrupts and exit commands
        - Integration with shared error handling and message formatting
        - Production-ready signal and exception handling
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
        # Use shared welcome message with terminal-specific formatting
        welcome_lines = WelcomeMessages.TERMINAL_WELCOME.strip().split("\n")

        # Add header with colored formatting
        header = f"""
{self._bold(self._blue("=" * 70))}
{self._bold(self._blue("        Personal Finance Tracker Agent"))}
{self._bold(self._blue("=" * 70))}
        """
        print(header)

        # Print the shared welcome message
        for line in welcome_lines:
            print(line)

        print(f"{self._bold(self._blue('-' * 70))}")

    def display_help(self) -> None:
        """
        Display help information for available commands and functionality.
        """
        # Use shared help message with terminal-specific formatting
        help_lines = WelcomeMessages.TERMINAL_HELP.strip().split("\n")

        for line in help_lines:
            print(line)

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

    def display_response(self, response: Dict[str, Any], verbose: bool = False) -> None:
        """
        Format and display the agent's response.

        Args:
            response: Dictionary containing the agent's response with keys:
                     - success: Boolean indicating execution success
                     - output: Agent's response message
                     - error: Error details if execution failed
            verbose: Whether to show technical details for debugging

        Formats the response with appropriate colors and icons based on success status.
        """
        print(f"\n{self._blue('🤖')} {self._bold('Finance Agent:')}")

        # Use shared error handler to process response
        output, is_success, error = AgentErrorHandler.process_agent_response(response)

        if is_success:
            print(f"{self._green('✅')} {output}")
        else:
            print(f"{self._red('❌')} {output}")

            # Show technical details if appropriate
            if AgentErrorHandler.should_show_technical_details(error, verbose):
                formatted_error = AgentErrorHandler.format_error_details(error)
                print(
                    f"{self._red('🔧')} {self._yellow('Technical details:')} {formatted_error}"
                )

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
        formatted_message = MessageFormatter.error_message(error_message)
        print(f"\n{formatted_message}")

    def display_info(self, info_message: str) -> None:
        """
        Display a formatted informational message.

        Args:
            info_message: The informational message to display
        """
        formatted_message = MessageFormatter.info_message(info_message)
        print(f"\n{formatted_message}")

    def run(self, agent: "FinanceAgent", verbose: bool = False) -> None:
        """
        Run the terminal interface main loop.

        Args:
            agent: The FinanceAgent instance to use for processing requests
            verbose: Whether verbose mode is enabled (used for error reporting)

        Handles the complete terminal interaction flow including:
        - Welcome display
        - User input loop
        - Agent request processing
        - Error handling and graceful shutdown
        """
        # Display welcome message
        self.display_welcome()

        try:
            # Main application loop
            while True:
                # Get user input (handles help and exit commands internally)
                user_input = self.get_user_input()

                # Check for exit condition
                if user_input is None:
                    break

                # Skip empty input (shouldn't happen due to validation in get_user_input)
                if not user_input.strip():
                    continue

                # Process request through agent
                try:
                    response = agent.execute_request(user_input)
                    self.display_response(response, verbose)
                except KeyboardInterrupt:
                    # Handle Ctrl+C during agent processing
                    interrupt_msg = AgentErrorHandler.handle_keyboard_interrupt()
                    print(
                        f"\n{interrupt_msg} You can continue with a new request or type 'quit' to exit."
                    )
                    continue
                except Exception as e:
                    # Handle unexpected errors during agent processing
                    error_msg = AgentErrorHandler.handle_unexpected_error(e)
                    error_response = {
                        "success": False,
                        "output": error_msg,
                        "error": str(e),
                    }
                    self.display_response(error_response, verbose)

        except KeyboardInterrupt:
            # Handle Ctrl+C in main loop
            print(f"\n\n👋 Goodbye! Thanks for using the Finance Tracker.")

        except Exception as e:
            # Handle any other unexpected errors
            formatted_error = MessageFormatter.error_message(f"Application error: {e}")
            print(f"\n{formatted_error}")
            print(
                MessageFormatter.info_message(
                    "Please restart the application and try again."
                )
            )
            sys.exit(1)

        # Display goodbye message for normal exit
        self.display_goodbye()
