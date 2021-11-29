from ..internal import BankAccount
from ..monitor import monitor
from datetime import datetime
from typing import Optional


class AgiosBankAccount(BankAccount):
    def __init__(self, owner: str, bank_account: "BankAccount", initial_balance: float = 0):
        super(AgiosBankAccount, self).__init__(owner, initial_balance)
        self.limit = 0
        self.bank_account: BankAccount = bank_account
        self.negative_date = None

    def __check_for_agios(self, current_time: datetime):
        if self.negative_date is not None:
            difference = current_time - self.negative_date
            agios = int(difference.days)
            print(agios)
            if agios > 0:
                self.bank_account._credit(agios, current_time)
                self.balance -= agios
                self.negative_date = None

    @monitor
    def transfer_to(self, recipient_account: "BankAccount", value: float, transaction_date: Optional[datetime] = None):
        if transaction_date is None:
            raise ValueError("Transaction date is compulsory for transfers with AgiosBankAccount")
        super(AgiosBankAccount, self).transfer_to(recipient_account, value, transaction_date)
        if self.balance - value < self.limit:
            self.negative_date = transaction_date

    def _credit(self, value: float, transaction_time: Optional[datetime]):
        super(AgiosBankAccount, self)._credit(value, transaction_time)
        self.__check_for_agios(transaction_time)

