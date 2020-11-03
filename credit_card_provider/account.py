from credit_card_provider import creditcard_exception


class Account:

    def __init__(self, user, credit_card_number: int, credit_card_limit: float):
        self.credit_card_limit = credit_card_limit
        self._balance = 0.0
        self._user = user
        self.account_id = credit_card_number

    def debit(self, amount: float):
        if self._balance + amount <= self.credit_card_limit:
            self._balance += amount

    def credit(self, amount):
        self._balance -= amount

    @property
    def credit_card_limit(self):
        return self._credit_card_limit

    @property
    def user(self):
        return self._user

    @credit_card_limit.setter
    def credit_card_limit(self, limit):
        if limit < 0:
            raise creditcard_exception.CreditCardException("Invalid Credit Card limit")
        self._credit_card_limit = limit

    @property
    def account_id(self) -> int:
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    @property
    def balance(self):
        return self._balance
