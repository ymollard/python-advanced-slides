from ..internal import BankAccount
import time


class AgiosBankAccount(BankAccount):
    def __init__(self, owner, bank_account, initial_balance=0):
        super(AgiosBankAccount, self).__init__(owner, initial_balance)
        self.limit = 0
        self.bank_account = bank_account
        self.negative_date = None

    def __check_for_agios(self):
        if self.negative_date is not None:
            difference = time.time() - self.negative_date
            agios = int(difference)
            if agios > 0:
                self.bank_account._credit(agios)
                self.balance -= agios
                self.negative_date = None

    def transfer_to(self, recipient_account, value):
        super(AgiosBankAccount, self).transfer_to(recipient_account, value)
        if self.balance - value < self.limit:
            self.negative_date = time.time()

    def _credit(self, value):
        super(AgiosBankAccount, self)._credit(value)
        self.__check_for_agios()

