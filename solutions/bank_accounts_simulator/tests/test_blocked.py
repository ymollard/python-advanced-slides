from account.external.blocked import BlockedBankAccount, UnauthorizedTransfer
import pytest


def test_unauthorized_transfer():
    account = BlockedBankAccount("owner", initial_balance=10)
    account2 = BlockedBankAccount("owner", initial_balance=0)
    with pytest.raises(UnauthorizedTransfer):
        account.transfer_to(account2, 11)
