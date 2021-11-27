from ..internal import BankAccount
from datetime import datetime
from typing import Optional


class UnauthorizedTransfer(ValueError):
    pass


class BlockedBankAccount(BankAccount):
    def __init__(self, owner, initial_balance=0):
        super(BlockedBankAccount, self).__init__(owner, initial_balance)
        self.limit = 0

    def transfer_to(self, recipient_account: "BankAccount", value: float, transaction_date: Optional[datetime] = None):
        if self.balance - value < self.limit:
            raise UnauthorizedTransfer(f"{self.owner} does not have enough money")
        super(BlockedBankAccount, self).transfer_to(recipient_account, value, transaction_date)
