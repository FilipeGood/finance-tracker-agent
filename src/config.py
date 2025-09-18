"""
Configuration Module

Centralized environment variable loading and validation for the Finance Tracker Agent.
Provides a single source of truth for application configuration with proper error handling.
"""

import os
from typing import Optional, Dict, Any


class ConfigurationError(Exception):
    """Raised when there's a configuration issue with environment variables."""

    pass


class AppConfig:
    """
    Application configuration manager.

    Handles loading and validation of environment variables required
    for different interfaces and components of the finance tracker.
    """

    @staticmethod
    def get_openai_api_key() -> str:
        """
        Get and validate OpenAI API key from environment.

        Returns:
            OpenAI API key string

        Raises:
            ConfigurationError: If API key is not found or empty
        """
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ConfigurationError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
            )
        return api_key

    @staticmethod
    def get_telegram_token() -> str:
        """
        Get and validate Telegram bot token from environment.

        Returns:
            Telegram bot token string

        Raises:
            ConfigurationError: If token is not found or empty
        """
        token = os.getenv("TG_TOKEN", "").strip()
        if not token:
            raise ConfigurationError(
                "TG_TOKEN environment variable is required for Telegram interface"
            )
        return token

    @staticmethod
    def validate_environment(interface_type: str = "terminal") -> Dict[str, Any]:
        """
        Validate environment variables for the specified interface.

        Args:
            interface_type: Type of interface ("terminal" or "telegram")

        Returns:
            Dictionary containing validated configuration values

        Raises:
            ConfigurationError: If required environment variables are missing
        """
        config = {}

        # OpenAI API key is required for both interfaces
        try:
            config["openai_api_key"] = AppConfig.get_openai_api_key()
        except ConfigurationError as e:
            raise ConfigurationError(
                f"{e}\n💡 Please ensure your OpenAI API key is set in the environment variables."
            )

        # Telegram token only required for telegram interface
        if interface_type == "telegram":
            try:
                config["telegram_token"] = AppConfig.get_telegram_token()
            except ConfigurationError as e:
                raise ConfigurationError(
                    f"{e}\n💡 Please set your Telegram bot token in the TG_TOKEN environment variable."
                )

        return config

    @staticmethod
    def validate_interface_selection(interface: str) -> str:
        """
        Validate interface selection parameter.

        Args:
            interface: Interface type to validate

        Returns:
            Validated interface string

        Raises:
            ConfigurationError: If interface is not supported
        """
        valid_interfaces = {"terminal", "telegram"}
        if interface not in valid_interfaces:
            raise ConfigurationError(
                f"Unsupported interface: {interface}. "
                f"Valid options are: {', '.join(sorted(valid_interfaces))}"
            )
        return interface
