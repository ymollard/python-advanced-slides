from datetime import datetime
from account.external.agios import AgiosBankAccount
from account.internal import BankAccount


def test_transfer_with_agios():
    bank = BankAccount("owner", 10000)
    account = AgiosBankAccount("owner", initial_balance=10, bank_account=bank)
    account2 = AgiosBankAccount("owner", initial_balance=0, bank_account=bank)
    account.transfer_to(account2, 11, datetime(2021, 11, 20))
    account2.transfer_to(account, 11, datetime(2021, 11, 21))
    assert bank.balance == 10001 and account.balance == 9


