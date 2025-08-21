from langchain_core.tools import tool
import json
from datetime import datetime
from pydantic import BaseModel
from src.schema import ExpenseInput, MainCategory, SubCategory
import pandas as pd
import os

CSV_PATH = "data/expenses.csv"


# Weather tool
@tool
def get_weather_tool(city: str) -> str:
    """Get current weather for a given city."""
    if city == "London":
        return "The current weather in London is cloudy and 15°C."
    elif city == "New York":
        return "The current weather in New York is rainy and 20°C."
    elif city == "Tokyo":
        return "The current weather in Tokyo is sunny and 30°C."
    else:
        return f"The current weather in {city} is sunny and 25°C."


# Current date tool
@tool
def get_current_date_tool() -> str:
    """Get the current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


@tool
def get_allowed_categories() -> dict[str, list[str]]:
    """Get allowed categories for expenses."""
    return {
        "main_categories": [category.value for category in MainCategory],
        "sub_categories": [category.value for category in SubCategory],
    }


@tool
def get_current_month_tool() -> str:
    """Get the current month in YYYY-MM format."""
    return datetime.now().strftime("%Y-%m")


@tool
def get_all_expenses() -> str:
    """Get all expenses from the CSV file."""

    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        return "No expenses found."

    df = pd.read_csv(CSV_PATH)

    # Convert DataFrame to JSON string
    expenses_json = df.to_json(orient="records", date_format="iso")
    return json.dumps(json.loads(expenses_json), indent=2)


@tool
def get_monthly_expenses(month: int):
    """Get expenses for a specific month."""
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        return "No expenses found."

    df = pd.read_csv(CSV_PATH)

    monthly_expenses = df[df["month"] == month]

    if monthly_expenses.empty:
        return f"No expenses found for month {month}."

    expenses_json = monthly_expenses.to_json(orient="records", date_format="iso")
    return json.dumps(json.loads(expenses_json), indent=2)


######################################################
################## Add // Update Expenses ############
######################################################


# Save expense tool with structured input
@tool
def save_expense_tool(expense_input: ExpenseInput) -> str:
    """
    Save an expense to the database.

    IMPORTANT: Use the exact enum values.

    Edge Cases:
        - Cigarettes and tobacco related expenses - main_category = OTHER, subcategory=OTHER
        - All restaurant bills, except for lunch at office, should be saved under main_category=RESTAURANT_NIGHT, sub_category=RESTAURANT_ENJOYMENT

    """
    df = pd.DataFrame([expense_input.model_dump()])

    # Check if file exists and has data rows
    file_has_data = os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0

    # Append to CSV with appropriate header
    df.to_csv(CSV_PATH, mode="a", header=not file_has_data, index=False)
    return (
        f"✅ Expense successfully saved with the following attributes:\n"
        f"📅 Date: {expense_input.year}-{expense_input.month:02d}\n"
        f"🏷️ Main Category: {expense_input.main_category.value}\n"
        f"🔖 Sub Category: {expense_input.sub_category.value}\n"
        f"🏦 Account: {expense_input.account.value}\n"
        f"💰 Amount: ${expense_input.amount:.2f}\n"
        f"📝 Note: {expense_input.note if expense_input.note else 'No note provided'}"
    )


@tool
def update_last_expense_attribute(attribute: str, value: str | float) -> str:
    """
    Update a specific attribute of the last saved expense.

    Args:
        attribute: The attribute to update (e.g., 'note', 'amount')
        value: The new value for the attribute

    Returns:
        String confirmation of the update with the new value
    """

    print(f"Updating last expense attribute: {attribute} to {value}")

    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        return "❌ No expenses found to update."

    # Read the CSV file
    df = pd.read_csv(CSV_PATH)

    if len(df) == 0:
        return "❌ No expenses found to update."

    # Get the last expense details before updating
    last_expense = df.iloc[-1].copy()

    # Update the specified attribute
    if attribute in df.columns:
        df.at[df.index[-1], attribute] = value

        last_expense = df.iloc[-1].copy()
        df.to_csv(CSV_PATH, index=False)

        return (
            f"✅ Last expense {attribute} successfully updated to '{value}'.\n"
            f"📅 Date: {last_expense['year']}-{last_expense['month']:02d}\n"
            f"🏷️ Main Category: {last_expense['main_category']}\n"
            f"🔖 Sub Category: {last_expense['sub_category']}\n"
            f"🏦 Account: {last_expense['account']}\n"
            f"💰 Amount: ${last_expense['amount']:.2f}\n"
            f"📝 Note: {last_expense['note'] if last_expense['note'] else 'No note provided'}"
        )
    else:
        return f"❌ Attribute '{attribute}' does not exist in the expense records."


######################################################
################## Get spending Report ##############
######################################################


@tool
def get_spendings_by_year_and_month() -> pd.DataFrame:
    """
    Update a specific attribute of the last saved expense.

    Args:

    Returns:
        pd.DataFrame: A DataFrame containing the spending data grouped by year and month. With columns: ['date', 'month', 'total_spent', 'average_spent', 'count']
    """
    df = pd.read_csv(CSV_PATH)

    df["month_number"] = df["month"].astype(int)
    df["month"] = pd.to_datetime(df["month_number"], format="%m").dt.strftime("%B")
    df["date"] = pd.to_datetime(
        df["year"].astype(str) + " " + df["month"], format="%Y %B"
    )

    ### 1. Spending by Year and Month
    by_year_month_df = (
        df.groupby([df["date"].dt.year, df["month_number"], df["month"]])
        .agg(
            total_spent=pd.NamedAgg(column="amount", aggfunc="sum"),
            average_spent=pd.NamedAgg(column="amount", aggfunc="mean"),
            count=pd.NamedAgg(column="amount", aggfunc="count"),
        )
        .sort_index(level=0)
        .reset_index()
    )
    by_year_month_df.drop("month_number", inplace=True, axis=1)

    return by_year_month_df


def _spendings_for_month(year: int, month: int, group_cols: list[str]) -> pd.DataFrame:
    """Internal helper to aggregate spendings for a given month.

    Args:
        year: target year (int)
        month: target month as integer (1-12)
        group_cols: list of column names to group by (e.g. ["main_category"], ["main_category", "sub_category"], ["account"]....).

    Returns:
        pd.DataFrame with columns = group_cols + ["total_spent", "average_spent", "count"]. Empty if no data.
    """
    df = pd.read_csv(CSV_PATH)
    if df.empty:
        return pd.DataFrame(
            columns=group_cols + ["total_spent", "average_spent", "count"]
        )

    # Build date for filtering (assuming month column stores full month name e.g. 'August')
    df["month"] = pd.to_datetime(df["month"], format="%m").dt.strftime("%B")
    df["date"] = pd.to_datetime(
        df["year"].astype(str) + " " + df["month"], format="%Y %B", errors="coerce"
    )
    # Filter by provided year & month integer
    filtered_df = df[(df["date"].dt.year == year) & (df["date"].dt.month == month)]

    if filtered_df.empty:
        return pd.DataFrame(
            columns=group_cols + ["total_spent", "average_spent", "count"]
        )

    grouped = (
        filtered_df.groupby(group_cols)
        .agg(
            total_spent=pd.NamedAgg(column="amount", aggfunc="sum"),
            average_spent=pd.NamedAgg(column="amount", aggfunc="mean"),
            count=pd.NamedAgg(column="amount", aggfunc="count"),
        )
        .reset_index()
    )
    return grouped


@tool
def get_spendings_by_category_for_specific_month(year: int, month: int) -> pd.DataFrame:
    """
    Get spending data for a specific month and year, grouped by category.

    Args:
        year (int): The year to filter by.
        month (int): The month to filter by.

    Returns:
        pd.DataFrame: A DataFrame containing the spending data for the specified month and year.
    """
    return _spendings_for_month(year, month, ["main_category"])


@tool
def get_spendings_by_main_and_subcategory_for_specific_month(
    year: int, month: int
) -> pd.DataFrame:
    """Get spending data for a specific month & year grouped by BOTH main_category and sub_category.

    Args:
        year (int): Year to filter (e.g. 2025)
        month (int): Month number 1-12 (e.g. 8 for August)

    Returns:
        pd.DataFrame: Columns [main_category, sub_category, total_spent, average_spent, count]. Empty if no data.
    """
    return _spendings_for_month(year, month, ["main_category", "sub_category"])


@tool
def get_spendings_by_account_for_specific_month(year: int, month: int) -> pd.DataFrame:
    """
    Get spending data for a specific month and year, grouped by account.

    Args:
        year (int): The year to filter by.
        month (int): The month to filter by.

    Returns:
        pd.DataFrame: A DataFrame containing the spending data for the specified month and year.
    """
    return _spendings_for_month(year, month, ["account"])
