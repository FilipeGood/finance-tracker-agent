import csv
from datetime import datetime
from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field


class MainCategory(str, Enum):
    """Main expense categories for financial tracking"""

    AP_HOUSE_EXPENSES = (
        "AP House Expenses"  # Utilities, maintenance for Armação de Pêra (AP) house
    )
    CAR_EXPENSE = "Car Expense"  # Vehicle costs: fuel, maintenance, insurance
    CORROIOS_HOUSE_EXPENSES = "Corroios House Expenses"  # Corroios property expenses
    DRINKS = "Drinks"  # Alcoholic beverages, bars, liquor purchases
    GROCERIES = "Groceries"  # Food shopping, household essentials
    LUNCH_OFFICE = "Lunch Office"  # Work-time meals and snacks
    OTHER = "Other"  # Cigarettes and tobacco related expenses
    PHONE = "Phone"  # Mobile phone bills and services
    RESTAURANT_NIGHT = "Restaurant Night"  # Dinner dining, special occasion meals
    VARIABLE = "Variable"  # Flexible discretionary spending


class SubCategory(str, Enum):
    """Detailed subcategories for expense classification"""

    AUTO_GAS = "Auto & Gas"  # Vehicle fuel and automotive expenses
    CLASSES = "Classes"  # Educational courses, lessons
    AIRBNB = "Airbnb"  # Short-term rental accommodations
    GEAR_CLOTHING = "Gear & Clothing"  # Apparel and equipment purchases
    GROCERIES = "Groceries"  # Food and household shopping
    HOME_IMPROVEMENTS = "Home Improvements"  # House renovation, repairs
    MORTGAGE = "Mortgage"  # Home loan payments
    PARKING = "Parking"  # Parking fees and permits
    PAYCHECK = "Paycheck"  # Salary income (positive entry)
    REPAIRS = "Repairs"  # General maintenance and fixes
    RESTAURANTS = "Restaurants"  # Dining out experiences
    STUFF = "Stuff"  # General miscellaneous items
    SUBSCRIPTIONS = "Subscriptions"  # Recurring service payments
    TRANSFER_MAIN_TO_SAVINGS = "Transfer from main to savings"  # Internal transfers
    TRAVEL = "Travel"  # Transportation, trips, vacations
    UTILITIES = "Utilities"  # Basic home services (electricity, water, gas)
    COFFEE = "Coffee"  # Coffee shop purchases
    PHONE = "Phone"  # Mobile phone services
    CAR_INSURANCE = "Car Insurance"  # Vehicle insurance premiums
    EDUCATION = "Education"  # Learning materials, courses
    BOOKS = "Books"  # Reading materials
    DOCTOR_DENTIST = "Doctor / Dentist"  # Healthcare appointments
    EMERGENCY_FUND = "Emergency Fund"  # Emergency savings
    FUN_ENTERTAINMENT = "Fun / Entertainment"  # Movies, concerts, games
    FURNITURE_APPLIANCES = "Furniture / Appliances"  # Home furnishings
    TRANSFER_SAVINGS_TO_MAIN = "Transfer savings to main"  # Internal transfers
    ICU_CAR = "ICU Car"  # Intensive car maintenance/repairs
    ELECTRICITY = "Electricity"  # Power bills
    WATER = "Water"  # Water utility bills
    AESTHETIC = "Aesthetic"  # Beauty treatments, cosmetics
    NETFLIX = "Netflix"  # Streaming services
    PRESENTS_FAMILY = "Presents Family"  # Gifts for family members
    TECH = "Tech"  # Technology purchases and services
    RENT = "Rent"  # Property rental payments
    OTHER = "Other"  # Uncategorized expenses
    TAXI = "Taxi"  # Taxi and ride services
    DRINKS = "Drinks"  # Alcoholic beverages
    SPORT = "Sport"  # Sports activities, equipment, gym memberships
    LUNCH_OFFICE = "Lunch Office"  # Work meal expenses
    RESTAURANT_ENJOYMENT = "Restaurant - Enjoyment"  # Leisure dining
    HAIRCUT = "Haircut"  # Hair styling and grooming
    UBER_EATS = "Uber Eats"  # Food delivery services
    VACATIONS = "Vacations"  # Holiday and travel expenses
    PARTY = "Party"  # Party supplies and entertainment
    HOUSE_PAYMENT = "House Payment"  # Mortgage or rent payments
    METRO = "Metro"  # Public transportation
    FINE_SS = "Fine SS"  # Social security or government fines
    HOME_INSURANCE = "Home Insurence"  # Property insurance
    APARTMENT = "Apartment"  # Apartment-related expenses
    BANK_COMMISSION = "Bank Comission"  # Banking fees
    LAUNDRY = "Laundry"  # Laundry services and supplies
    VET = "Vet"  # Veterinary services for pets
    GROCERIES_REVOLUT = "Groceries Revolut"  # Groceries paid via Revolut
    AP_HOME_UTILITIES = "AP Home Utilities"  # AP property utility bills
    REVOLUT = "Revolut"  # Revolut-specific transactions
    FITNESS = "Fitness"  # Gym, personal training, fitness equipment


class Account(str, Enum):
    """Account types for expense tracking"""

    MAIN = "Main"  # Primary checking/spending account
    SAVINGS = "Savings"  # Savings account for long-term storage


class ExpenseInput(BaseModel):
    """Input model for recording financial expenses with intelligent defaults"""

    year: int = Field(
        default_factory=lambda: datetime.now().year, description="Year of the expense"
    )
    month: int = Field(
        default_factory=lambda: datetime.now().month, description="Month of the expense"
    )
    main_category: MainCategory = Field(
        default=MainCategory.OTHER, description="Main category of the expense"
    )
    sub_category: SubCategory = Field(
        default=SubCategory.OTHER, description="Sub-category of the expense"
    )
    account: Account = Field(
        default=Account.MAIN, description="Account used for the expense"
    )

    amount: float = Field(..., gt=0, description="Amount spent (must be positive)")
    note: str = Field(default="", description="Optional note about the expense")
