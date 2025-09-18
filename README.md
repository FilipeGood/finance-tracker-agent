
# Finance Tracker Agent

A personal finance tracker agent that uses natural language processing to track expenses, analyze spending patterns, and provide financial insights. Built with LangChain and OpenAI GPT models.

This project provides a unified interface supporting both terminal and Telegram interactions for expense tracking and financial analysis.

## Features

- **Natural Language Processing**: Interact using everyday language to track expenses
- **Multi-Interface Support**: Choose between terminal or Telegram interfaces
- **Expense Management**: Add, update, and analyze your financial data
- **Smart Categorization**: Automatic expense categorization with customizable categories
- **Financial Insights**: Get spending reports and financial analysis
- **Data Persistence**: CSV-based data storage for your expense records

## Example Interactions

The agent can handle natural language commands like:
- "Add new expense in a restaurant 56 euros today"
- "Give me my spendings for the last month" 
- "Analyze my spendings over the last month"
- "Analyse my spendings and tell me insights and what I should do better"
- "Get the spendings by category for this current month"
- "Based on my expenses, can you tell me financial insights?"

## Quick Start

### Prerequisites
1. Python 3.8+ with pipenv installed
2. OpenAI API key
3. (Optional) Telegram Bot Token for Telegram interface

### Installation
1. Install dependencies:
   ```bash
   pipenv install --dev
   ```

2. Set up environment variables in `.env` file:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   TG_TOKEN=your_telegram_bot_token_here  # Only needed for Telegram interface
   ```

### Usage

#### Terminal Interface (Default)
```bash
# Basic usage
pipenv run python3 main.py

# With verbose output to see agent reasoning
pipenv run python3 main.py --verbose

# Explicitly specify terminal interface
pipenv run python3 main.py --interface terminal --verbose
```

#### Telegram Interface
```bash
# Start Telegram bot
pipenv run python3 main.py --interface telegram
```

### Command Line Options
- `--interface`: Choose interface type (`terminal` or `telegram`, default: `terminal`)
- `-v, --verbose`: Enable verbose output to see agent's internal reasoning and tool calls
## Project Structure

```
├── main.py                     # Unified application entry point
├── src/                        # Core application modules
│   ├── __init__.py            # Package initialization and exports
│   ├── agent.py               # Main FinanceAgent class
│   ├── config.py              # Configuration and environment validation
│   ├── terminal_interface.py  # Terminal interface implementation
│   ├── telegram_interface.py  # Telegram bot interface implementation
│   ├── tools.py               # Financial analysis and management tools
│   ├── feedback.py            # User feedback and message formatting
│   ├── schema.py              # Data schemas and validation
│   └── ...                    # Other supporting modules
├── data/
│   └── expenses.csv           # Expense data storage
├── notebooks/                 # Development and testing notebooks
│   ├── analysis/              # Feature testing and development
│   │   ├── add_update_expenses_tools/    # Expense management tools testing
│   │   ├── spending_report_tool/         # Spending report generation testing  
│   │   ├── custom-agent-scratch/         # Custom agent learning experiments
│   │   └── langchain_agents/             # LangChain agent implementation examples
│   └── test_finance_agent.ipynb          # Main testing notebook
├── Pipfile                    # Python dependencies
└── README.md                  # This file
```

### Core Components

- **main.py**: Unified entry point supporting both terminal and Telegram interfaces
- **src/agent.py**: Core FinanceAgent class powered by LangChain and OpenAI
- **src/tools.py**: Financial tools for expense tracking, categorization, and analysis
- **src/terminal_interface.py**: Interactive terminal interface with colored output
- **src/telegram_interface.py**: Telegram bot interface with markdown formatting
- **src/config.py**: Environment configuration and validation utilities




### Data Structure
The system tracks expenses with the following attributes:
- Year and Month
- Main Category (Car Expense, Groceries, Restaurant Night, etc.)
- Sub Category (Auto & Gas, Groceries, Restaurant - Enjoyment, etc.)
- Account (Main Account, Food Account, etc.)
- Amount and Notes



## Testing & Examples

The agent supports various natural language commands for expense management:

### Basic Operations
1. **Add Expense**: "Can you add a new expense of dinner out for 10€? With note 'testing agent'"
2. **Update Expense**: "Can you update the sub category of the last expense to the value 'Drinks'?"
3. **Get Categories**: "What are the allowed categories?"

### Reporting & Analysis  
4. **Monthly Reports**: "Based on my expenses in the csv file, can you do a monthly spending report of the last 3 months only? We are in august"
5. **Category Breakdown**: "Can I get the spendings by category for the current month?"
6. **Detailed Category Analysis**: "Can I get the spendings by category and sub_category for this current month?"
7. **Account Analysis**: "Can I get the spendings by account for this current month?"
8. **Comprehensive Report**: "Can I get the full and detailed spending report for this current month? Include as much info as possible"

### Testing Interfaces

To test both interfaces:

**Terminal Interface:**
```bash
pipenv run python3 main.py --verbose
# Then try the example commands above
```

**Telegram Interface:**
```bash  
pipenv run python3 main.py --interface telegram
# Send the example commands to your Telegram bot
```