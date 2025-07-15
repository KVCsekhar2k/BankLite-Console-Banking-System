import json
import uuid
from datetime import datetime

class Account:
    def __init__(self, id, name, balance=0, transactions=None):
        self.id = id
        self.name = name
        self.balance = balance
        self.transactions = transactions if transactions else []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            log = f"{datetime.now()}: Deposited ₹{amount} | Balance ₹{self.balance}"
            self.transactions.append(log)
            print(f" {log}")
        else:
            print(" Invalid deposit amount.")

    def withdraw(self, amount):
        if amount <= 0:
            print(" Invalid withdrawal amount.")
        elif amount > self.balance:
            print(" Insufficient funds.")
        else:
            self.balance -= amount
            log = f"{datetime.now()}: Withdrawn ₹{amount} | Balance ₹{self.balance}"
            self.transactions.append(log)
            print(f" {log}")

    def get_balance(self):
        print(f"Account [{self.id}] - {self.name} | Current Balance: ₹{self.balance}")

    def get_history(self):
        print(f"Transaction History for {self.name}:")
        for transaction in self.transactions:
            print(transaction)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'balance': self.balance,
            'transactions': self.transactions
        }

    @staticmethod
    def from_dict(data):
        return Account(
            id=data['id'],
            name=data['name'],
            balance=data['balance'],
            transactions=data['transactions']
        )


class Bank:
    def __init__(self):
        self.accounts = []

    def create_account(self, name):
        account_id = str(uuid.uuid4())[:8]
        account = Account(account_id, name)
        self.accounts.append(account)
        print(f" Account created for {name} | Account Number: {account_id}")

    def find_account_by_id(self, account_id):
        for account in self.accounts:
            if account.id == account_id:
                return account
        print(" Account not found.")
        return None

    def deposit_to_account(self, account_id, amount):
        account = self.find_account_by_id(account_id)
        if account:
            account.deposit(amount)

    def withdraw_from_account(self, account_id, amount):
        account = self.find_account_by_id(account_id)
        if account:
            account.withdraw(amount)

    def show_account_details(self, account_id):
        account = self.find_account_by_id(account_id)
        if account:
            account.get_balance()
            account.get_history()

    def save_to_file(self, filename='bank.json'):
        data = [account.to_dict() for account in self.accounts]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(" Data saved successfully.")

    def load_from_file(self, filename='bank.json'):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.accounts = [Account.from_dict(acc) for acc in data]
            print(" Data loaded successfully.")
        except FileNotFoundError:
            print(" No existing data found. Starting fresh.")

# ----------- Main Program -----------

def main():
    bank = Bank()
    bank.load_from_file()

    while True:
        print("\n BankLite Menu:")
        print("1️ Create Account")
        print("2️ Deposit")
        print("3️ Withdraw")
        print("4️ View Account Details")
        print("5️ Save & Exit")

        choice = input("Select option (1-5): ")

        if choice == '1':
            name = input("Enter Account Holder Name: ")
            bank.create_account(name)

        elif choice == '2':
            acc_id = input("Enter Account ID: ")
            amount = float(input("Enter amount to deposit: ₹"))
            bank.deposit_to_account(acc_id, amount)

        elif choice == '3':
            acc_id = input("Enter Account ID: ")
            amount = float(input("Enter amount to withdraw: ₹"))
            bank.withdraw_from_account(acc_id, amount)

        elif choice == '4':
            acc_id = input("Enter Account ID: ")
            bank.show_account_details(acc_id)

        elif choice == '5':
            bank.save_to_file()
            print(" Data saved successfully.")
            again = input("Do you want to perform another operation? (y/n): ").lower()
            if again == 'y':
                continue 
            else:
                print(" Thank you for using BankLite. Goodbye!")
                break


        else:
            print(" Invalid choice. Please select from 1-5.")

if __name__ == "__main__":
    main()
