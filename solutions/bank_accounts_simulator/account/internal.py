from typing import Optional
from datetime import datetime


class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0):
        self.balance = initial_balance
        self.owner = owner

    def transfer_to(self, recipient_account: "BankAccount", value: float, transaction_date: Optional[datetime] = None):
        self.balance -= value
        recipient_account._credit(value, transaction_date)

    def _credit(self, value: float, transaction_time: Optional[datetime]):
        self.balance += value

    def print(self):
        print(f"This account owned by {self.owner} has a balance of ${self.balance}")

