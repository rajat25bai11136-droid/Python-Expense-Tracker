import csv
import os
from datetime import datetime

# --- Configuration ---
CSV_FILE = 'expenses.csv'
CATEGORIES = ['Food', 'Transport', 'Utilities', 'Entertainment', 'Other']
# ---------------------

def initialize_csv():
    """Checks if the CSV file exists and creates it with headers if not."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Amount', 'Category', 'Description'])
        print(f"Created new data file: {CSV_FILE}")

def add_expense():
    """Prompts the user for expense details and writes them to the CSV file."""
    print("\n--- Add New Expense ---")
    
    # 1. Get Amount
    while True:
        try:
            amount = float(input("Enter amount (e.g., 50.75): "))
            if amount <= 0:
                print("Amount must be positive.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # 2. Get Category
    print("\nAvailable Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
        
    while True:
        try:
            choice = int(input(f"Enter category number (1-{len(CATEGORIES)}): "))
            if 1 <= choice <= len(CATEGORIES):
                category = CATEGORIES[choice - 1]
                break
            else:
                print("Invalid choice. Please select a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    # 3. Get Description and Date
    description = input("Enter a brief description (e.g., Coffee, Bus fare): ")
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 4. Write to CSV
    try:
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date_str, amount, category, description])
        print("\n✅ Expense successfully recorded!")
    except Exception as e:
        print(f"❌ Error writing to file: {e}")


def view_summary():
    """Reads all expenses from the CSV and prints a category-wise summary."""
    print("\n--- Expense Summary ---")
    
    if not os.path.exists(CSV_FILE):
        print("No expense data found. Add an expense first.")
        return

    expenses_by_category = {cat: 0.0 for cat in CATEGORIES}
    total_expenses = 0.0
    
    try:
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader) # Skip the header row
            
            # Read and process data
            for row in reader:
                try:
                    # Expecting: Date, Amount, Category, Description
                    date, amount_str, category, desc = row
                    amount = float(amount_str)
                    
                    if category in expenses_by_category:
                        expenses_by_category[category] += amount
                    total_expenses += amount
                except (ValueError, IndexError):
                    print(f"Warning: Skipping corrupted row: {row}")
                    continue

        # Print detailed breakdown
        print("\nCategory Breakdown:")
        for cat, total in expenses_by_category.items():
            if total > 0:
                # Calculate percentage
                percentage = (total / total_expenses) * 100 if total_expenses > 0 else 0
                print(f"- {cat:<15}: ${total:,.2f} ({percentage:.1f}%)")

        print("\n" + "="*30)
        print(f"TOTAL SPENT: ${total_expenses:,.2f}")
        print("="*30)
        
    except Exception as e:
        print(f"❌ An error occurred while reading the file: {e}")


def main_menu():
    """Displays the main menu and handles user selection."""
    initialize_csv() # Ensure the data file exists
    
    while True:
        print("\n===============================")
        print("    DAILY EXPENSE TRACKER")
        print("===============================")
        print("1. Add New Expense")
        print("2. View Summary Report")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            print("\n👋 Thank you for using the tracker. Goodbye!")
            break
        else:
            print("\n🛑 Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()