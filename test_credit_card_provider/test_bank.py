import unittest
from credit_card_provider import bank
from unittest.mock import patch


class BankTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_bank = bank.Bank()

    def create_valid_test_account(self):
        test_input = "Add Tom 4111111111111111 $1000"
        self.test_bank.execute(test_input)

    def create_invalid_test_account(self):
        test_input = "Add Quincy 1234567890123456 $2000"
        self.test_bank.execute(test_input)

    @patch('credit_card_provider.user')
    def test_create_account(self, test_user):
        test_user.name = "test_user"
        self.test_bank.create_account("4111111111111111", test_user, 1000)
        self.assertIn("test_user", self.test_bank._valid_accounts)
        test_user.associate.assert_called_once()

    @patch('credit_card_provider.user')
    def test_invalid_create_account(self, test_user):
        test_user.name = "test_invalid_user"
        self.test_bank.create_account("1234567890123456", test_user, 1000)
        self.assertIn("test_invalid_user", self.test_bank._invalid_accounts)
        test_user.associate.assert_not_called()

    def test_execute_add(self):
        self.create_valid_test_account()
        self.assertIn("Tom", self.test_bank._valid_accounts)

    def test_execute_invalid_add(self):
        self.create_invalid_test_account()
        self.assertIn("Quincy", self.test_bank._invalid_accounts)

    def test_execute_charge(self):
        self.create_valid_test_account()
        test_input = "Charge Tom $500"
        self.test_bank.execute(test_input)
        tom_account = self.test_bank._valid_accounts["Tom"]
        self.assertEqual(tom_account.balance, 500)

    def test_execute_over_charge(self):
        self.create_valid_test_account()
        test_input = "Charge Tom $1500"
        self.test_bank.execute(test_input)
        tom_account = self.test_bank._valid_accounts["Tom"]
        self.assertEqual(tom_account.balance, 0)

    @patch('credit_card_provider.account.Account')
    def test_execute_invalid_charge(self, mock_account):
        self.create_invalid_test_account()
        test_input = "Charge Quincy $1500"
        self.test_bank.execute(test_input)
        mock_account.assert_not_called()

    def test_execute_credit(self):
        self.create_valid_test_account()
        test_input = "Charge Tom $500"
        self.test_bank.execute(test_input)
        test_credit_input = "Credit Tom $200"
        self.test_bank.execute(test_credit_input)
        tom_account = self.test_bank._valid_accounts["Tom"]
        self.assertEqual(tom_account.balance, 300)

    def test_execute_negative_credit(self):
        self.create_valid_test_account()
        test_input = "Charge Tom $500"
        self.test_bank.execute(test_input)
        test_credit_input = "Credit Tom $700"
        self.test_bank.execute(test_credit_input)
        tom_account = self.test_bank._valid_accounts["Tom"]
        self.assertEqual(tom_account.balance, -200)


if __name__ == '__main__':
    unittest.main()
