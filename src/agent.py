"""
Finance Agent Module

This module contains the FinanceAgent class that encapsulates the agent creation,
configuration, and execution for the personal finance tracker.
"""

import traceback

import os
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from src.tools import (
    save_expense_tool,
    get_current_date_tool,
    get_current_month_tool,
    get_all_expenses,
    get_allowed_categories,
    get_monthly_expenses,
    update_last_expense_attribute,
    get_spendings_by_year_and_month,
    get_spendings_by_category_for_specific_month,
    get_spendings_by_main_and_subcategory_for_specific_month,
    get_spendings_by_account_for_specific_month,
)
from src.prompts import openai_functions_agent_prompt


class FinanceAgent:
    """
    Finance Agent for expense tracking and financial analysis.

    This class encapsulates the configuration and execution of a LangChain agent
    that can handle expense tracking, updates, and financial reporting through
    natural language interactions.
    """

    def __init__(self, model: str = "gpt-3.5-turbo", verbose: bool = False):

        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
            )

        self.llm = ChatOpenAI(model=model, api_key=api_key)

        self.tools = [
            save_expense_tool,
            get_current_date_tool,
            get_current_month_tool,
            get_monthly_expenses,
            get_all_expenses,
            update_last_expense_attribute,
            get_spendings_by_year_and_month,
            get_allowed_categories,
            get_spendings_by_category_for_specific_month,
            get_spendings_by_main_and_subcategory_for_specific_month,
            get_spendings_by_account_for_specific_month,
        ]

        self.prompt = openai_functions_agent_prompt

        self.agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=verbose,
            handle_parsing_errors=True,
        )

    def execute_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user request and return the agent's response.

        Args:
            user_input: Natural language input from the user

        Returns:
            Dictionary containing:
                - success: Boolean indicating if execution was successful
                - output: Agent's response or error message
                - error: Error details if execution failed

        Example:
            >>> agent = FinanceAgent()
            >>> result = agent.execute_request("Add new expense in a restaurant 56 euros today")
            >>> print(result['output'])
        """
        try:
            # Execute the agent with user input
            result = self.agent_executor.invoke({"input": user_input})

            return {
                "success": True,
                "output": result.get("output", "No output received"),
                "error": None,
            }

        except Exception as e:
            # Handle agent execution errors
            error_message = "".join(
                traceback.format_exception(type(e), e, e.__traceback__)
            )

            return {
                "success": False,
                "output": "I encountered an error while processing your request. Please try again or rephrase your request.",
                "error": error_message,
            }

    def get_available_tools(self) -> list[str]:
        """
        Get list of available tool names.

        Returns:
            List of tool names that the agent can use
        """
        return [tool.name for tool in self.tools]

    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the configured LLM.

        Returns:
            Dictionary with model information
        """
        return {"model_name": self.llm.model_name, "model_type": "ChatOpenAI"}
