import unittest
from credit_card_provider import bank
from unittest.mock import patch


class BankTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_bank = bank.Bank()

    def create_valid_test_account(self):
        test_input = "Add Tom Home 4111111111111111 $1000"
        self.test_bank.execute(test_input)

    def create_invalid_test_account(self):
        test_input = "Add Quincy Home 1234567890123456 $2000"
        self.test_bank.execute(test_input)

    @patch('credit_card_provider.user')
    def test_create_account(self, test_user):
        test_user.name = "test_user"
        self.test_bank.create_account("4111111111111111", test_user, "Home", 1000)
        self.assertIn(("test_user", "Home"), self.test_bank._valid_accounts)
        test_user.associate.assert_called_once()

    @patch('credit_card_provider.user')
    def test_invalid_create_account(self, test_user):
        test_user.name = "test_invalid_user"
        self.test_bank.create_account("1234567890123456", test_user, "Home", 1000)
        self.assertIn(("test_invalid_user", "Home"), self.test_bank._invalid_accounts)
        test_user.associate.assert_not_called()

    def test_execute_add(self):
        self.create_valid_test_account()
        self.assertIn(("Tom", "Home"), self.test_bank._valid_accounts)

    def test_execute_invalid_add(self):
        self.create_invalid_test_account()
        self.assertIn(("Quincy", "Home"), self.test_bank._invalid_accounts)

    def test_execute_charge(self):
        self.create_valid_test_account()
        test_input = "Charge Tom Home $500"
        self.test_bank.execute(test_input)
        tom_account = self.test_bank._valid_accounts[("Tom", "Home")]
        self.assertEqual(tom_account.balance, 500)

    def test_execute_over_charge(self):
        self.create_valid_test_account()
        test_input = "Charge Tom Home $1500"
        self.test_bank.execute(test_input)
        tom_account = self.test_bank._valid_accounts[("Tom", "Home")]
        self.assertEqual(tom_account.balance, 0)

    @patch('credit_card_provider.account.Account')
    def test_execute_invalid_charge(self, mock_account):
        self.create_invalid_test_account()
        test_input = "Charge Quincy Home $1500"
        self.test_bank.execute(test_input)
        mock_account.assert_not_called()

    def test_execute_credit(self):
        self.create_valid_test_account()
        test_input = "Charge Tom Home $500"
        self.test_bank.execute(test_input)
        test_credit_input = "Credit Tom Home $200"
        self.test_bank.execute(test_credit_input)
        tom_account = self.test_bank._valid_accounts[("Tom", "Home")]
        self.assertEqual(tom_account.balance, 300)

    def test_execute_negative_credit(self):
        self.create_valid_test_account()
        test_input = "Charge Tom Home $500"
        self.test_bank.execute(test_input)
        test_credit_input = "Credit Tom Home $700"
        self.test_bank.execute(test_credit_input)
        tom_account = self.test_bank._valid_accounts[("Tom", "Home")]
        self.assertEqual(tom_account.balance, -200)

    def test_add_account_tag(self):
        test_input = "Add Tom Home 4111111111111111 $1000"
        self.test_bank.execute(test_input)
        self.assertIn(("Tom", "Home"), self.test_bank._valid_accounts)

    def test_transaction_log(self):
        test_input = "Add Lisa Work 4111111111111111 $7"
        expected_log = ["Lisa: (Work) $0"]
        self.test_bank.execute(test_input)
        actual_log = self.test_bank.transaction_log()
        self.assertEqual(expected_log, actual_log)

    def test_transaction_log_multi_tag(self):
        test_input1 = "Add Lisa Work 4111111111111111 $7"
        self.test_bank.execute(test_input1)
        test_input2 = "Add Lisa Gold 378282246310005 $71"
        self.test_bank.execute(test_input2)
        expected_log = ["Lisa: (Gold) $0, (Work) $0"]
        actual_log = self.test_bank.transaction_log()
        self.assertEqual(expected_log, actual_log)


if __name__ == '__main__':
    unittest.main()
