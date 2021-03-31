from credit_card_provider.user import User
from credit_card_provider.account import Account
from luhn import verify
from collections import ChainMap
from collections import defaultdict


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
    def create_account(self, credit_card_number, user: User, tag: str, limit: float) -> None:
        if Bank.validate_card(credit_card_number):
            account = Account(user, credit_card_number, limit, tag)
            user.associate(account)
            self._valid_accounts[(user.name, tag)] = account
        else:
            self._invalid_accounts[(user.name, tag)] = None

    # executes the transaction statement with the provided format
    def execute(self, transaction: str) -> None:
        transaction_details = transaction.split(' ')
        if transaction_details[0] == 'Add':
            user = User(transaction_details[1])
            tag = transaction_details[2]
            limit = Bank.sanitize_amount(transaction_details[4])
            self.create_account(transaction_details[3], user, tag, limit)
        if transaction_details[0] == 'Charge':
            if (transaction_details[1], transaction_details[2]) in self._valid_accounts:
                account = self._valid_accounts[(transaction_details[1], transaction_details[2])]
                amount = Bank.sanitize_amount(transaction_details[3])
                account.debit(amount)
        if transaction_details[0] == "Credit":
            if (transaction_details[1], transaction_details[2]) in self._valid_accounts:
                account = self._valid_accounts[(transaction_details[1], transaction_details[2])]
                amount = Bank.sanitize_amount(transaction_details[3])
                account.credit(amount)

    # prints the transactions/history in alphabetical order
    def transaction_log(self):
        output = []
        hMap = defaultdict(list)
        all_accounts = ChainMap(self._valid_accounts, self._invalid_accounts)
        for account_details, account in sorted(all_accounts.items(), key=lambda x: x[0][0].lower()):
            account_name, account_tag = account_details

            if not account:
                hMap[account_name].append((account_tag, None))
            else:
                hMap[account_name].append((account_tag, account.balance))

        for account_name, account_details in hMap.items():
            account_details.sort(key=lambda x: x[0])
            account_det = []
            for indv_account in account_details:
                account_tag, balance = indv_account
                if balance is None:
                    account_det.append(f"({account_tag}) error")
                else:
                    account_det.append(f"({account_tag}) ${int(balance)}")
            account_list = ', '.join(account_det)
            output.append(f"{account_name}: {account_list}")
        return output
