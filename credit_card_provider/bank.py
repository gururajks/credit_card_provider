from credit_card_provider.user import User
from credit_card_provider.account import Account
from luhn import verify


class Bank:

    def __init__(self):
        self._valid_accounts = {}
        self._invalid_accounts = {}

    # validate the credit card number based on the luhn 10 check.
    @classmethod
    def validate_card(cls, card_number) -> bool:
        return verify(card_number)

    # cleans the amount as it can prefixes like '$' and such
    @classmethod
    def sanitize_amount(cls, number) -> float:
        if number[0] == '$':
            number = number[1:]
        return float(number)

    # creates a bank account and adds the registers it within the bank object
    # creates an association between user and account as well
    def create_account(self, credit_card_number, user: User, limit: float) -> None:
        if Bank.validate_card(credit_card_number):
            account = Account(user, credit_card_number, limit)
            user.associate(account)
            self._valid_accounts[user.name] = account
        else:
            self._invalid_accounts[user.name] = None

    # executes the transaction statement with the provided format
    def execute(self, transaction: str) -> None:
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

    # prints the transactions/history in alphabetical order
    def transaction_log(self) -> None:
        all_accounts = {**self._valid_accounts, **self._invalid_accounts}
        display = []
        # display the user irrespective of the user's name (caps or lower)
        for account_name, account in all_accounts.items():
            if not account:
                display.append((account_name.lower(), account_name, None))
            else:
                display.append((account_name.lower(), account_name, account.balance))
        display.sort(key=lambda x: x[0])
        for _, account_name, account_balance in display:
            if account_balance is None:
                print(f"{account_name}:     Error")
            else:
                print(f"{account_name}:     {account_balance: .2f}")
