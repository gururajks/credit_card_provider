import unittest
from credit_card_provider import account
from credit_card_provider import user


class TestAccount(unittest.TestCase):

    def setUp(self) -> None:
        self.test_user = user.User("Test User")
        self.test_account = account.Account(self.test_user, 4111111111111111, 1000)

    def test_debit(self):
        self.test_account.debit(100)
        self.assertEqual(100, self.test_account.balance)
        self.test_account.debit(200)
        self.assertEqual(300, self.test_account.balance)

    def test_credit(self):
        self.test_account.debit(500)
        self.assertEqual(500, self.test_account.balance)
        self.test_account.credit(300)
        self.assertEqual(200, self.test_account.balance)

    def test_negative_credit(self):
        self.test_account.debit(500)
        self.assertEqual(500, self.test_account.balance)
        self.test_account.credit(600)
        self.assertEqual(-100, self.test_account.balance)


if __name__ == '__main__':
    unittest.main()
