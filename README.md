
# Finance Tracker Agent

A personal finance tracker agent that uses natural language processing to track expenses, analyze spending patterns, and provide financial insights. Built with LangChain and OpenAI GPT models.

The ultimate goal of this project is to have an agent, integrated with telegram chat, that can track expensing, analyze git rm --cached .env
Examples of interactions with the Telegram Agent:
   - "Add new expense in a restaurant 56 euros today"
   - "Give me my spendings for the last month"
   - "Analyze my spendings over the last month"
   - "Analyse my spendings and tell me insights and what I should do better."
   - "Get the spendings by category for this current month"
   - "Based on my expenses, can you tell me financial insights?"

Therefore, this project requires:
1. Telegram integration - should be able to read messages from a telegram channel and send messages back
2. LLM Agent:
   a) Analyze the natural language message
   b) Decide which tools to use in order to accomplish the user goal
   c) Return a structured answer



## Getting started
1. Install dependencies : pipenv install --dev
2. Add your OPENAI API Key to .env
3. pipenv run python3 main.py --verbose
## Project Structure

- data/expenses.csv - Expense data storage

- notebooks - Development and testing notebooks - where all .ipynb file are stored
  - notebooks/analysis - used for testing new features before adding them to the main code
      - /add_update_expenses_tools - notebook used to test the add expense and update expense tools
      - /spending_report_tool - notebbok to test the generation of spending report using the tools
      - /custom-agent-scratch - notebook with a custom agent built from scratch for learning purposes
      - /langchain_agents - notebook with multiple ways/methods to implement agents with langchain
- `/src/` - all python files that are used across the project




### Data Structure
The system tracks expenses with the following attributes:
- Year and Month
- Main Category (Car Expense, Groceries, Restaurant Night, etc.)
- Sub Category (Auto & Gas, Groceries, Restaurant - Enjoyment, etc.)
- Account (Main Account, Food Account, etc.)
- Amount and Notes



### Tests

1. Add Expense : " Can you add a new expense of dinner out for 10€? With note 'testing agent' "
2. Update Expense: "Can you update the sub category of the last expense to the value 'Drinks'?"  ❌ 
3. Get allowed cats: "What are the allowed categories?"
4. Get spendings by year and month: Based on my expenses in the csv file, can you do a monthly spending report of the last 3 months only? We are in august
5. Get spendings by category: Can I get the spendings by category for the current month?
6. Get spendings by category and sub category: Can I get the spendings by category and sub_category for this current month?
7. Get spendings by account for specific month: Can I get the spendings by account for this current month?
8. Full Monthly report: Can I get the full and detailed spending report for this current month? Include as much info as possible