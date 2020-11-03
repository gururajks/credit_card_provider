from credit_card_provider.user import User
from credit_card_provider.account import Account
from credit_card_provider import creditcard_exception
from luhn import verify


class Bank:

    def __init__(self):
        self._all_accounts = {}

    @classmethod
    def validate_card(cls, card_number):
        return verify(card_number)

    def create_account(self, credit_card_number, user: User):
        if Bank.validate_card(credit_card_number):
            account = Account(user, credit_card_number)
            user.assosiate(account)
            self._all_accounts[user.name] = account
        else:
            raise creditcard_exception.CreditCardException("Credit Card number not valid")

    def execute(self, transaction):
        transaction_details = transaction.split(' ')
        if transaction_details[0] == 'Add':
            user = User(transaction_details[1])
            self.create_account(transaction_details[2], user)
            user.deposit(transaction_details[2], transaction_details[3])
        if transaction_details[0] == 'Charge':
            if transaction_details[1] in self._all_accounts:
                account = self._all_accounts[transaction_details[1]]
                account.debit(transaction_details[2])
        if transaction_details[0] == "Credit":
            if transaction_details[1] in self._all_accounts:
                account = self._all_accounts[transaction_details[1]]
                account.credit(transaction_details[2])
