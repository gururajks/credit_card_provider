import uuid
from credit_card_provider.account import Account


class User:
    def __init__(self, name):
        self._id = uuid.uuid4().hex
        self._name = name
        self._accounts = {}

    def charge(self, account_id, amount):
        account = self._accounts[account_id]
        account.debit(amount)

    def deposit(self, account_id, amount):
        account = self._accounts[account_id]
        account.credit(amount)

    def assosiate(self, account: Account):
        self._accounts[account.account_id] = account

    @property
    def name(self):
        return self._name
