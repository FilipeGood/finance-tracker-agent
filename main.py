"""
Unified Main Application Entry Point

This module serves as the unified entry point for the Personal Finance Tracker Agent,
supporting both terminal and Telegram interfaces through a single command-line interface.
The application coordinates the FinanceAgent with the selected interface to provide
expense tracking and financial analysis capabilities.

Features:
    - Unified CLI with --interface selection (terminal/telegram)
    - Shared agent initialization and error handling
    - Graceful shutdown handling for both interfaces
    - Production-ready configuration validation
    - Verbose mode support for debugging

Usage:
    python main.py --interface terminal --verbose
    python main.py --interface telegram
"""

import sys
import signal
import argparse
from typing import Optional

# Terminal interface imports
from src.agent import FinanceAgent
from src.terminal_interface import TerminalInterface

# Telegram interface imports
from src.telegram_interface import TelegramInterface

# Shared modules
from src.config import AppConfig, ConfigurationError
from src.feedback import MessageFormatter


def signal_handler(signum: int, frame) -> None:
    """
    Handle system signals for graceful shutdown.

    Args:
        signum: Signal number received
        frame: Current stack frame
    """
    print(f"\n👋 Received shutdown signal. Exiting gracefully...")
    sys.exit(0)


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
        print(
            MessageFormatter.configuration_error_message(
                str(e),
                "Please ensure your OpenAI API key is set in the environment variables.",
            )
        )
        return None
    except Exception as e:
        # Unexpected initialization errors
        print(
            MessageFormatter.error_message(f"Failed to initialize Finance Agent: {e}")
        )
        return None


def parse_arguments():
    """
    Parse command line arguments for interface selection and options.

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
    parser.add_argument(
        "--interface",
        choices=["terminal", "telegram"],
        default="terminal",
        help="Interface to use for interaction (default: terminal)",
    )
    return parser.parse_args()


def main() -> None:
    """
    Main application entry point that handles interface selection and coordination.

    Parses command line arguments, validates configuration, initializes the agent,
    and routes to the appropriate interface based on user selection. Handles
    graceful shutdown on system signals.
    """
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Parse command line arguments
    args = parse_arguments()

    # Validate interface selection and environment configuration
    try:
        interface_type = AppConfig.validate_interface_selection(args.interface)
        config = AppConfig.validate_environment(interface_type)
    except ConfigurationError as e:
        print(str(e))
        sys.exit(1)

    # Initialize agent
    agent = initialize_agent(verbose=args.verbose)
    if not agent:
        print(
            MessageFormatter.error_message(
                "Cannot start the application without a properly configured agent."
            )
        )
        sys.exit(1)

    # Route to appropriate interface
    if args.interface == "terminal":
        terminal = TerminalInterface(use_colors=True)
        terminal.run(agent, args.verbose)
    elif args.interface == "telegram":
        telegram = TelegramInterface()
        telegram.run(agent)
    else:
        # This should not happen due to validation above, but included for completeness
        print(
            MessageFormatter.error_message(f"Unsupported interface: {args.interface}")
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
