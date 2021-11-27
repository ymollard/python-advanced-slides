from ..internal import BankAccount


class BlockedBankAccount(BankAccount):
    def __init__(self, owner, initial_balance=0):
        super(BlockedBankAccount, self).__init__(owner, initial_balance)
        self.limit = 0

    def transfer_to(self, recipient_account, value):
        if self.balance - value < self.limit:
            raise ValueError("{} does not have enough money".format(self.owner))
        super(BlockedBankAccount, self).transfer_to(recipient_account, value)
