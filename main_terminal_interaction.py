"""
Main Application Entry Point

This module serves as the entry point for the Personal Finance Tracker Agent,
coordinating the FinanceAgent and TerminalInterface to provide a complete
command-line experience for expense tracking and financial analysis.
"""

import sys
import argparse
from typing import Optional

from src.agent import FinanceAgent
from src.terminal_interface import TerminalInterface


def initialize_agent(verbose: bool = False) -> Optional[FinanceAgent]:
    """
    Initialize the Finance Agent with error handling.

    Args:
        verbose: Enable verbose output for agent execution

    Returns:
        FinanceAgent instance, or None if initialization fails
    """
    try:
        agent = FinanceAgent(model="gpt-3.5-turbo", verbose=verbose)
        return agent
    except ValueError as e:
        # Environment/API key errors
        print(f"❌ Configuration Error: {e}")
        print(
            "💡 Please ensure your OpenAI API key is set in the environment variables."
        )
        return None
    except Exception as e:
        # Unexpected initialization errors
        print(f"❌ Failed to initialize Finance Agent: {e}")
        return None


def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Personal Finance Tracker Agent - Track expenses and analyze spending with natural language"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output to see agent's internal reasoning and tool calls",
    )
    return parser.parse_args()


def main() -> None:
    """
    Main application loop that coordinates the agent and terminal interface.

    Handles user interaction, processes requests through the agent,
    and displays formatted responses until the user exits.
    """
    # Parse command line arguments
    args = parse_arguments()

    # Initialize components
    agent = initialize_agent(verbose=args.verbose)
    if not agent:
        print("🚫 Cannot start the application without a properly configured agent.")
        sys.exit(1)

    terminal = TerminalInterface(use_colors=True)

    # Display welcome message
    terminal.display_welcome()

    try:
        # Main application loop
        while True:
            # Get user input (handles help and exit commands internally)
            user_input = terminal.get_user_input()

            # Check for exit condition
            if user_input is None:
                break

            # Skip empty input (shouldn't happen due to validation in get_user_input)
            if not user_input.strip():
                continue

            # Process request through agent
            try:
                response = agent.execute_request(user_input)
                terminal.display_response(response)
            except KeyboardInterrupt:
                # Handle Ctrl+C during agent processing
                print(
                    f"\n⚠️ Request interrupted. You can continue with a new request or type 'quit' to exit."
                )
                continue
            except Exception as e:
                # Handle unexpected errors during agent processing
                error_response = {
                    "success": False,
                    "output": "An unexpected error occurred while processing your request.",
                    "error": str(e),
                }
                terminal.display_response(error_response)

    except KeyboardInterrupt:
        # Handle Ctrl+C in main loop
        print(f"\n\n👋 Goodbye! Thanks for using the Finance Tracker.")

    except Exception as e:
        # Handle any other unexpected errors
        print(f"\n❌ Application error: {e}")
        print("🔄 Please restart the application and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
