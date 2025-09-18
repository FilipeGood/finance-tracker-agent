"""
Personal Finance Tracker Agent

A modular personal finance tracking application with natural language processing
capabilities for expense tracking, analysis, and financial insights.

Core Components:
- agent: Main FinanceAgent class for natural language processing
- config: Application configuration and environment validation
- tools: Financial tools for expense management and analysis
- interface modules: Terminal and Telegram interfaces
- feedback: User feedback and message formatting utilities

Usage:
    from src.agent import FinanceAgent
    from src.terminal_interface import TerminalInterface
    from src.telegram_interface import TelegramInterface
"""

__version__ = "1.0.0"
__author__ = "Finance Tracker Agent Team"

# Core exports
from .agent import FinanceAgent
from .config import AppConfig, ConfigurationError
from .terminal_interface import TerminalInterface
from .telegram_interface import TelegramInterface
from .feedback import MessageFormatter

__all__ = [
    "FinanceAgent",
    "AppConfig",
    "ConfigurationError",
    "TerminalInterface",
    "TelegramInterface",
    "MessageFormatter",
]
