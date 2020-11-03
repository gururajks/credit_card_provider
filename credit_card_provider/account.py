from credit_card_provider import creditcard_exception
from credit_card_provider import bank

class Account:

    def __init__(self, user, credit_card_number: int):
        self._balance = 0.0
        self._user = user
        self.account_id = credit_card_number

    @property
    def account_id(self) -> int:
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        if not bank.Bank.validate_card(account_id):
            raise creditcard_exception.CreditCardException("Account number is not valid")
        self._account_id = account_id

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if type(amount) == str and amount[0] == '$':
            amount = amount[1:]
        self._balance = int(amount)

    def debit(self, amount: int):
        if self.balance - amount < 0:
            raise creditcard_exception.CreditCardException("not enough balance")
        self._balance -= amount

    def credit(self, amount):
        self._balance += amount
