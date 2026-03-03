"""
Personal Finance Tracker
========================
A command-line application for tracking personal income and expenses
with data visualization capabilities.

Author: ABHI VARSHITHA CHOWDARY
Date: February 2026
Python Version: 3.x
"""
import json
from datetime import datetime
import os

INCOME_CATEGORIES = ['Freelancing', 'Salary', 'Gift', 'Investment', 'Others']
EXPENSE_CATEGORIES = ['Food', 'Grocery', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Health', 'Others']

TRANSACTIONS_FILE = "transactions.json"

def load_transactions():
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "r") as file:
            return json.load(file)
    return []

def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, "w") as file:
        json.dump(transactions, file, indent = 4)

def generate_id(transactions):
    if len(transactions) == 0:
        return 1
    return max(t["id"] for t in transactions) + 1


def add_transaction(transaction_type):
    """
    Add a new income or expense transaction
    
    Args:
        transaction_type: "income" or "expense"
    """
    print(f"\n--- ADD {transaction_type.upper()} ---")
    
    # Get amount
    try:
        amount = float(input("Amount: $"))
        if amount <= 0:
            print("Amount must be positive!")
            return
    except ValueError:
        print("Invalid amount! Please enter a number.")
        return
    
    # Get category
    categories = INCOME_CATEGORIES if transaction_type == "income" else EXPENSE_CATEGORIES
    
    print("\nCategories:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    try:
        cat_choice = int(input("\nChoose category (number): "))
        if 1 <= cat_choice <= len(categories):
            category = categories[cat_choice - 1]
        else:
            print("Invalid category!")
            return
    except ValueError:
        print("Please enter a valid number!")
        return
    
    # Get description
    description = input("Description: ").strip()
    if description == "":
        description = f"{category} {transaction_type}"
    
    # Get date (smart default!)
    date_input = input("Date (press Enter for today, or YYYY-MM-DD): ").strip()
    
    if date_input == "":
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        # TODO: Validate date format
        date = date_input
    
    # Create transaction
    transaction = {
        "id": generate_id(transactions),
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    transactions.append(transaction)
    save_transactions(transactions)
    
    print(f"\n✓ {transaction_type.capitalize()} of ${amount:.2f} added!")

def view_all_transactions():
    """Display all transactions sorted by date"""
    if len(transactions) == 0:
        print("\nNo transactions yet! Add your first transaction.")
        return
    
    print("\n" + "="*70)
    print("                    ALL TRANSACTIONS")
    print("="*70)
    
    # Sort by date (newest first)
    sorted_transactions = sorted(transactions, key=lambda x: x["date"], reverse=True)
    
    for t in sorted_transactions:
        # Format display
        trans_type = "📈" if t["type"] == "income" else "📉"
        sign = "+" if t["type"] == "income" else "-"
        
        print(f"\n{trans_type} ID: {t['id']} | {t['date']}")
        print(f"   {t['category']}: {sign}${t['amount']:.2f}")
        print(f"   {t['description']}")
    
    print("\n" + "="*70)

def monthly_summary():
    """Show summary for current month"""
    if len(transactions) == 0:
        print("\nNo transactions yet!")
        return
    
    # Get current month/year
    now = datetime.now()
    current_month = now.strftime("%Y-%m")  # e.g., "2026-02"
    
    # Calculate totals
    total_income = 0
    total_expenses = 0
    
    for t in transactions:
        # Check if transaction is from current month
        if t["date"].startswith(current_month):
            if t["type"] == "income":
                total_income += t["amount"]
            else:
                total_expenses += t["amount"]
    
    savings = total_income - total_expenses
    
    # Display summary
    print("\n" + "="*50)
    print(f"       SUMMARY FOR {now.strftime('%B %Y')}")
    print("="*50)
    print(f"\n💰 Total Income:    ${total_income:,.2f}")
    print(f"💸 Total Expenses:  ${total_expenses:,.2f}")
    print(f"{'─'*50}")
    
    if savings >= 0:
        print(f"💚 Savings:         ${savings:,.2f}")
    else:
        print(f"⚠️  Deficit:         ${abs(savings):,.2f}")
    
    print("\n" + "="*50)

def expense_breakdown():
    """Show pie chart of expenses by category"""
    import matplotlib.pyplot as plt
    
    if len(transactions) == 0:
        print("\nNo transactions yet!")
        return
    
    # Calculate spending by category
    expense_by_category = {}
    
    for t in transactions:
        if t["type"] == "expense":
            category = t["category"]
            if category not in expense_by_category:
                expense_by_category[category] = 0
            expense_by_category[category] += t["amount"]
    
    if len(expense_by_category) == 0:
        print("\nNo expenses recorded yet!")
        return
    
    # Prepare data for chart
    categories = list(expense_by_category.keys())
    amounts = list(expense_by_category.values())
    
    # Create pie chart
    plt.figure(figsize=(10, 7))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title('Expense Breakdown by Category', fontsize=16, fontweight='bold')
    plt.axis('equal')  # Equal aspect ratio ensures circle
    plt.tight_layout()
    plt.show()
    
    print("\n✓ Chart displayed!")

def income_vs_expenses_chart():
    """Show bar chart comparing income and expenses"""
    import matplotlib.pyplot as plt
    
    if len(transactions) == 0:
        print("\nNo transactions yet!")
        return
    
    # Group by month
    monthly_data = {}
    
    for t in transactions:
        month = t["date"][:7]  # Get YYYY-MM
        
        if month not in monthly_data:
            monthly_data[month] = {"income": 0, "expenses": 0}
        
        if t["type"] == "income":
            monthly_data[month]["income"] += t["amount"]
        else:
            monthly_data[month]["expenses"] += t["amount"]
    
    # Prepare data
    months = sorted(monthly_data.keys())
    income_amounts = [monthly_data[m]["income"] for m in months]
    expense_amounts = [monthly_data[m]["expenses"] for m in months]
    
    # Create bar chart
    x = range(len(months))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    plt.bar([i - width/2 for i in x], income_amounts, width, label='Income', color='green', alpha=0.8)
    plt.bar([i + width/2 for i in x], expense_amounts, width, label='Expenses', color='red', alpha=0.8)
    
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Amount ($)', fontsize=12)
    plt.title('Income vs Expenses by Month', fontsize=16, fontweight='bold')
    plt.xticks(x, months)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print("\n✓ Chart displayed!")
# Load existing transactions
transactions = load_transactions()

print("="*50)
print("        PERSONAL FINANCE TRACKER")
print("="*50)

# Main menu loop
while True:
    print("\n--- MAIN MENU ---")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View All Transactions")
    print("4. Monthly Summary")
    print("5. Expense Breakdown Chart")      # ← NEW
    print("6. Income vs Expenses Chart")     # ← NEW
    print("7. Exit")                         # ← Changed from 5 to 7
    
    choice = input("\nChoose option (1-7): ")
    
    if choice == "1":
        add_transaction("income")
    
    elif choice == "2":
        add_transaction("expense")
    
    elif choice == "3":
        view_all_transactions()
    
    elif choice == "4":
        monthly_summary()
    
    elif choice == "5":
        expense_breakdown()
    
    elif choice == "6":
        income_vs_expenses_chart()
    
    elif choice == "7":
        print("\n💾 All transactions saved!")
        print("Keep tracking your finances! 💰")
        break
    
    else:
        print("Invalid choice! Please enter 1-7.")