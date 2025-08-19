
# Finance Tracker Agent

A personal finance tracker agent that uses natural language processing to track expenses, analyze spending patterns, and provide financial insights. Built with LangChain and OpenAI GPT models.

## Features

### 1.  Expense Management
- **Add Expenses**: Process natural language commands to save expenses
- **Update Expenses**: Modify attributes of previously saved expenses
- **Expense Retrieval**: Get all or filtered expenses from the database

### 2. Spending Analysis & Reports
- **Monthly Reports**: Get detailed spending breakdowns by month
- **Category Analysis**: View expenses grouped by main and sub-categories
- **Account-based Reports**: Track spending across different accounts
- **Multi-month Comparisons**: Analyze spending trends over time

### Data Structure
The system tracks expenses with the following attributes:
- Year and Month
- Main Category (Car Expense, Groceries, Restaurant Night, etc.)
- Sub Category (Auto & Gas, Groceries, Restaurant - Enjoyment, etc.)
- Account (Main Account, Food Account, etc.)
- Amount and Notes

## Project Structure

- `/src/` - Core application modules (tools, schema, prompts)
- `/notebooks/` - Development and testing notebooks
  - `add_update_expenses_tools.ipynb` - Expense management functionality
  - `spending_report_tool.ipynb` - Reporting and analysis features
- `/data/expenses.csv` - Expense data storage

## Example Interactions

- "Add new expense in a restaurant of 56 euros today"
- "Save a $80 grocery shopping expense"
- "Fix the last expense month 7"
- "Can you do a monthly spending report of the last 3 months?"
- "Get the spendings by category for this current month"
- "Based on my expenses, can you tell me financial insights?"

## Requirements

- Python 3.12
- OpenAI API key
- Dependencies managed via Pipfile (LangChain, OpenAI, Pandas, etc.)
