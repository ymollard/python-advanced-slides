from account.internal import BankAccount


def test_authorized_transfer():
    account = BankAccount("owner", initial_balance=10)
    account2 = BankAccount("owner", initial_balance=10)
    account.transfer_to(account2, 15)
    assert account.balance == 10 - 15 and account2.balance == 10 + 15

