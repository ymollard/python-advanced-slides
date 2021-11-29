from functools import wraps


def monitor(f):
    """
    This is a decorator for BankAccounts child classes warning the user if no transfer of that amount
    has been executed before by that owner
    """
    monitor.thresholds = {}

    @wraps(f)   # @wraps ensures the decorated function still behave as the original e.g. for its __doc__
    def __wrapper_function(self, recipient_account, value, transaction_date):
        if self.owner not in monitor.thresholds:
            monitor.thresholds[self.owner] = 50
        if value > monitor.thresholds[self.owner]:
            print(f"⚠ This is the first time that {self.owner} performs such a big transaction (${value})")
            monitor.thresholds[self.owner] = value
        f(self, recipient_account, value, transaction_date)
    return __wrapper_function
