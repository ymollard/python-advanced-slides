from account.external.agios import AgiosBankAccount
from account.external.blocked import BlockedBankAccount
from account.internal import BankAccount
from datetime import datetime

bank = BankAccount("HSBC", 10000)
walmart = BlockedBankAccount("Walmart", 5000)
alice = BlockedBankAccount("Alice Dupont", 500)
bob = AgiosBankAccount("Bob Müller", bank, 100)

alice.transfer_to(walmart, 100, datetime(2021, 11, 20))
bob.transfer_to(walmart, 90, datetime(2021, 11, 20))
alice.transfer_to(walmart, 100, datetime(2021, 11, 21))
bob.transfer_to(walmart, 150, datetime(2021, 11, 21))
alice.transfer_to(bob, 300, datetime(2021, 11, 26))

for account in [bank, walmart, alice, bob]:
    account.print()

