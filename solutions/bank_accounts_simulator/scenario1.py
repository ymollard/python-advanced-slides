from account.external.agios import AgiosBankAccount
from account.external.blocked import BlockedBankAccount
from account.internal import BankAccount
import time

bank = BankAccount("HSBC", 10000)
walmart = AgiosBankAccount("Walmart", 5000)
alice = BlockedBankAccount("Alice Dupont", 500)
bob = AgiosBankAccount("Bob Müller", bank, 100)

alice.transfer_to(walmart, 100)
bob.transfer_to(walmart, 100)
alice.transfer_to(bob, 100)
bob.transfer_to(walmart, 150)
time.sleep(5)
alice.transfer_to(bob, 100)

for account in [bank, walmart, alice, bob]:
    account.print()

