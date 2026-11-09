"""
Codomax Digital Internship - Module 03
Object-Oriented Python: Banking System

Features:
- Create bank accounts
- Deposit money
- Withdraw money
- View account details and transaction history
- Demonstrates classes, objects, constructors, methods,
  encapsulation, inheritance, polymorphism, and abstraction.

Data is stored in a local JSON file named bank_data.json.
No external packages are required.
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("bank_data.json")


# -------------------- ABSTRACTION --------------------

class BankAccountBase(ABC):
    """Abstract base class for bank accounts."""

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass


# -------------------- BASE CLASS --------------------

class BankAccount(BankAccountBase):
    """A basic bank account."""

    def __init__(self, account_number, holder_name, opening_balance=0.0):
        self.account_number = account_number
        self.holder_name = holder_name
        self._balance = float(opening_balance)  # Encapsulated attribute
        self._transactions = []

        if self._balance < 0:
            raise ValueError("Opening balance cannot be negative.")

        if self._balance > 0:
            self._record_transaction("Opening balance", self._balance)

    def _record_transaction(self, transaction_type, amount):
        """Private-style helper method to record account activity."""
        self._transactions.append({
            "type": transaction_type,
            "amount": round(float(amount), 2),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def deposit(self, amount):
        """Add money to the account."""
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self._balance += amount
        self._record_transaction("Deposit", amount)
        return self._balance

    def withdraw(self, amount):
        """Withdraw money if sufficient balance is available."""
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if amount > self._balance:
            raise ValueError("Insufficient balance.")

        self._balance -= amount
        self._record_transaction("Withdrawal", amount)
        return self._balance

    def get_balance(self):
        """Return the current balance without exposing the stored attribute."""
        return round(self._balance, 2)

    def get_transactions(self):
        """Return a copy of transaction history."""
        return list(self._transactions)

    def account_type(self):
        """Return the account type. Overridden by child classes."""
        return "General"

    def to_dict(self):
        """Convert account data to a JSON-compatible dictionary."""
        return {
            "account_type": self.account_type(),
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "balance": self._balance,
            "transactions": self._transactions
        }


# -------------------- INHERITANCE --------------------

class SavingsAccount(BankAccount):
    """Savings account derived from BankAccount."""

    def account_type(self):
        # Polymorphism: same method name, different implementation.
        return "Savings"


class CurrentAccount(BankAccount):
    """Current account derived from BankAccount."""

    def account_type(self):
        # Polymorphism: same method name, different implementation.
        return "Current"


# -------------------- BANK / FILE HANDLING --------------------

class Bank:
    """Manages accounts and saves/loads them from a JSON file."""

    def __init__(self):
        self.accounts = {}
        self.load_data()

    def create_account(self, account_type, account_number, holder_name, opening_balance):
        if account_number in self.accounts:
            raise ValueError("That account number already exists.")

        account_classes = {
            "savings": SavingsAccount,
            "current": CurrentAccount
        }

        account_class = account_classes.get(account_type.lower())
        if account_class is None:
            raise ValueError("Account type must be Savings or Current.")

        account = account_class(account_number, holder_name, opening_balance)
        self.accounts[account_number] = account
        self.save_data()
        return account

    def find_account(self, account_number):
        account = self.accounts.get(account_number)
        if account is None:
            raise ValueError("Account not found.")
        return account

    def save_data(self):
        try:
            data = [account.to_dict() for account in self.accounts.values()]
            with DATA_FILE.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except OSError as error:
            print(f"Could not save bank data: {error}")

    def load_data(self):
        if not DATA_FILE.exists():
            return

        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                account_class = (
                    SavingsAccount if item.get("account_type") == "Savings"
                    else CurrentAccount
                )
                account = account_class(
                    item["account_number"],
                    item["holder_name"],
                    item.get("balance", 0)
                )
                account._transactions = item.get("transactions", [])
                self.accounts[account.account_number] = account

        except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"Could not load saved bank data: {error}")


# -------------------- USER INTERFACE --------------------

def read_amount(prompt):
    try:
        amount = float(input(prompt))
        if amount <= 0:
            raise ValueError
        return amount
    except ValueError:
        raise ValueError("Enter a valid amount greater than zero.")


def show_account(account):
    print("\\n--- Account Details ---")
    print(f"Account number: {account.account_number}")
    print(f"Account holder: {account.holder_name}")
    print(f"Account type: {account.account_type()}")
    print(f"Available balance: {account.get_balance():.2f}")


def show_transactions(account):
    transactions = account.get_transactions()
    print("\\n--- Transaction History ---")
    if not transactions:
        print("No transactions available.")
        return

    for transaction in transactions:
        print(
            f"{transaction['date']} | {transaction['type']} | "
            f"{transaction['amount']:.2f}"
        )


def main():
    bank = Bank()

    while True:
        print("\\n========== PYTHON BANKING SYSTEM ==========")
        print("1. Create account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. View account details")
        print("5. View transaction history")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        try:
            if choice == "1":
                account_type = input("Account type (Savings/Current): ").strip()
                account_number = input("Choose account number: ").strip()
                holder_name = input("Account holder name: ").strip()
                if not account_number or not holder_name:
                    raise ValueError("Account number and name are required.")

                opening_balance = float(input("Opening balance: "))
                account = bank.create_account(
                    account_type, account_number, holder_name, opening_balance
                )
                print(f"{account.account_type()} account created successfully.")

            elif choice in {"2", "3", "4", "5"}:
                account_number = input("Enter account number: ").strip()
                account = bank.find_account(account_number)

                if choice == "2":
                    amount = read_amount("Amount to deposit: ")
                    account.deposit(amount)
                    bank.save_data()
                    print(f"Deposit successful. Balance: {account.get_balance():.2f}")

                elif choice == "3":
                    amount = read_amount("Amount to withdraw: ")
                    account.withdraw(amount)
                    bank.save_data()
                    print(f"Withdrawal successful. Balance: {account.get_balance():.2f}")

                elif choice == "4":
                    show_account(account)

                elif choice == "5":
                    show_transactions(account)

            elif choice == "6":
                bank.save_data()
                print("Thank you for using the Python Banking System.")
                break

            else:
                print("Invalid choice. Please select 1-6.")

        except (ValueError, TypeError) as error:
            print(f"Error: {error}")
        except (KeyboardInterrupt, EOFError):
            print("\\nProgram stopped safely.")
            bank.save_data()
            break


if __name__ == "__main__":
    main()
