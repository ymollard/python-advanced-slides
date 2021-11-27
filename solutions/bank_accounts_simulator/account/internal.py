class BankAccount:
    def __init__(self, owner, initial_balance=0):
        self.balance = initial_balance
        self.owner = owner

    def transfer_to(self, recipient_account, value):
        self.balance -= value
        recipient_account._credit(value)

    def _credit(self, value):
        self.balance += value

    def print(self):
        print(f"This account owned by {self.owner} has a balance of ${self.balance}")

