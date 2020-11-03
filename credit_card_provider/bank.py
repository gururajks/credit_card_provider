from credit_card_provider.user import User
from credit_card_provider.account import Account
from luhn import verify


class Bank:

    def __init__(self):
        self._valid_accounts = {}
        self._invalid_accounts = {}

    @classmethod
    def validate_card(cls, card_number):
        return verify(card_number)

    @classmethod
    def sanitize_amount(cls, number):
        if number[0] == '$':
            number = number[1:]
        return float(number)

    def create_account(self, credit_card_number, user: User, limit: float):
        if Bank.validate_card(credit_card_number):
            account = Account(user, credit_card_number, limit)
            user.associate(account)
            self._valid_accounts[user.name] = account
        else:
            self._invalid_accounts[user.name] = None

    def execute(self, transaction: str):
        transaction_details = transaction.split(' ')
        if transaction_details[0] == 'Add':
            user = User(transaction_details[1])
            limit = Bank.sanitize_amount(transaction_details[3])
            self.create_account(transaction_details[2], user, limit)
        if transaction_details[0] == 'Charge':
            if transaction_details[1] in self._valid_accounts:
                account = self._valid_accounts[transaction_details[1]]
                amount = Bank.sanitize_amount(transaction_details[2])
                account.debit(amount)
        if transaction_details[0] == "Credit":
            if transaction_details[1] in self._valid_accounts:
                account = self._valid_accounts[transaction_details[1]]
                amount = Bank.sanitize_amount(transaction_details[2])
                account.credit(amount)

    def transaction_log(self):
        for account_name, account in self._valid_accounts.items():
            print(f"{account_name}:     {account.balance: .2f}")
        for account_name, account in self._invalid_accounts.items():
            print(f"{account_name}:      Error")
