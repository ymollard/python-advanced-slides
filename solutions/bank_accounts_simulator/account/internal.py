from typing import Optional
from datetime import datetime
import matplotlib.pyplot as plt


class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0):
        self.balance = initial_balance
        self.history = []
        self.owner = owner

    def transfer_to(self, recipient_account: "BankAccount", value: float, transaction_date: Optional[datetime] = None):
        self.balance -= value
        self.history.append(self.balance)
        recipient_account._credit(value, transaction_date)

    def _credit(self, value: float, transaction_time: Optional[datetime]):
        self.balance += value
        self.history.append(self.balance)

    def print(self):
        print(f"This account owned by {self.owner} has a balance of ${self.balance}")

    def plot(self):
        plt.plot(range(len(self.history)), self.history, label=f"Balance history for {self.owner}")
